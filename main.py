from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_request
import generic_helper

app = FastAPI()

inprogress_orders = {}

@app.post("/")
async def handle_request(request: Request):
    # reterive the json data from the request
    payload = await request.json()
    # print(payload)
    # exit()
    # Extract the necessary information from the payload
    # based on the webhookrequest dialog flow structure
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    # print("this is your params",parameters)
    output_contexts = payload['queryResult']['outputContexts']

    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])

    intent_handler_dict = {
        'order.add - contexts: ongoing-order' : add_to_order,
        'order.remove - contexts: ongoing-order' : remove_from_order,
        'order.complete - contexts: ongoing-order' : complete_order,
        'track.order - contexts : ongoing-tracking' : track_order
    }
    return intent_handler_dict[intent](parameters, session_id)

def remove_from_order(parameters: dict, session_id: str):
    print(parameters)
    if session_id not in inprogress_orders:
        return JSONResponse(content ={
        "fulfillmentText" : "I'm having trouble finding your order. Sorry! Can you place a new order"
    } )

    current_order = inprogress_orders[session_id]
    food_items = parameters["food-items"]

    removed_items = []
    no_such_items = []

    for items in food_items:
        if items not in current_order:
            no_such_items.append(items)
        else:
            removed_items.append(items)
            del current_order[items]
    if len(removed_items) > 0:
        fulfillment_text = f'Removed {",".join(removed_items)} from your order'
    
    if len(no_such_items) > 0:
        fulfillment_text = f'your current order does not have {",".join(no_such_items)}'
    
    if len(current_order.keys()) == 0:
        fulfillment_text += "Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f"Here is what is left in your order: {order_str}"
    
    return JSONResponse(content ={
        "fulfillmentText" : fulfillment_text
    } )

def save_to_db(order: dict):
    next_order_id = db_request.get_next_order_id()
    
    for food_item, quantity in order.items():
        rcode = db_request.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )
        if rcode == -1:
            return -1
        
    db_request.insert_order_tracking(next_order_id, "in progress")
    return next_order_id

def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having a trouble finding your order.Sorry! can you place order again"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)

        if order_id == -1:
            fulfillment_text = "Sorry!, I couldn't process your order due to backend error." \
                 " Please place a new order again"
            
        else:
            order_total = db_request.get_total_order_price(order_id)
            fulfillment_text = f"Awesome. We have placed your order." \
                                f"Here is your order id # {order_id}." \
                                f"Your order total is {order_total} which you can pay at the time of delivery!"

        del inprogress_orders[session_id]

    return JSONResponse(content ={
        "fulfillmentText" : fulfillment_text
    } )


def add_to_order(parameters: dict, session_id: str):
    food_items = parameters["food-items"]
    food_quantities = parameters ["number"]

    if len(food_items) != len(food_quantities):
        fulfillment_text = "sorry I didn't understand. Can you please specify food items and quantities"
    else:
        new_food_dict = dict(zip(food_items, food_quantities))

        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict
        
        # print(f"this is session with food dict {inprogress_orders}")

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"so far you have: {order_str}. do you want anything else ?"
        # fulfillment_text = f"Received {food_items} and {food_quantities} in the backend"

    return JSONResponse(content ={
        "fulfillmentText" : fulfillment_text
    } )


def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['number'])
    order_status =  db_request.get_order_status(order_id)

    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id:{order_id}"

    return JSONResponse(content ={
            "fulfillmentText" : fulfillment_text
        } )
    