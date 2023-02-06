# -*- coding: utf-8 -*-
"""
Backend Designs for Bank of Singapore's Queuing System

@author: WreckioNg
"""
from flask import Flask, request, render_template
from data_structure import *
from werkzeug.exceptions import HTTPException
import copy

"""
Declare and instantiate data structure.
"""

# [FIXED] Assign the data structure object and stored it in memory
cache = []

# [FIXED] Assign the branch_no and its corresponding branch_name_dict for mapping
branch_no_list = [x.upper() for x in ['Branch-A','Branch-B','Branch-C']]
branch_name_dict = {'BRANCH-A':'Jurong Point'
                    , 'BRANCH-B':'Orchard'
                    , 'BRANCH-C':'Changi Airport'}

# [FIXED] Assign the business_type and its corresponding business_name_dict for mapping
business_type_list = ['A','B','C']
business_name_dict = {'A':'Retail Banking'
                     , 'B':'Private Banking'
                     , 'C':'Corporate Banking'}

# [FLEXIBLE] Predefined the data structure for bos's bank service
for i in branch_no_list:
    bank_obj = BankMap(i)
    for j in business_type_list:
        biz_obj = BizQueue(j)

        biz_obj.addCounter(1)
        biz_obj.addCounter(2)
        biz_obj.addCounter(3)

        bank_obj.addList(biz_obj)

    cache.append(bank_obj)

###
# The following part are for Flask object and application design
###

"""
Create a Flask object.
"""

###
# Initialize the Flask app
# Set extensions for css and img file
###

app = Flask(__name__, template_folder = './static/templates')# , static_folder="")

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
'''
"""
Handle 500 Error.
"""
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e

    # Handle the 500 internal error, defined as a wrong input url
    return """
        <html>
            Please check your url again!
        </html>
    """
'''

"""
Routes for display screen.
"""
@app.route('/www.bos.com/display/<url_branch_no>/<url_biz_type>', methods = ['GET', 'POST'])
def displaySPA(url_branch_no, url_biz_type):
    url_branch_no = url_branch_no.upper()
    url_biz_type = url_biz_type.upper()
    target_bank = [x for x in cache if x.branch_no == url_branch_no][0]
    target_biz = [y for y in target_bank.biz_list if y.biz_type == url_biz_type][0]
    target_call_list = copy.deepcopy(target_biz.call_list)
    
    print(target_call_list)
    # Generate call list for jinja parameters
    if target_call_list:
        while len(target_call_list) < 3:
            target_call_list.append(['—','—'])
    else:
        target_call_list = [['—','—'], ['—','—'], ['—','—']]
    # Generate queue list for jinja parameters
    if target_biz.queue_list == []:
        html_queue_list = "Nobody in queue."
    else:
        html_queue_list = " - ".join([str(x.queue_no) for x in target_biz.queue_list])
    
    # Generate missed list for jinja parameters
    if target_biz.queue_list == []:
        html_missed_list = "Nobody missed call."
    else:
        html_missed_list = " - ".join([str(x.queue_no) for x in target_biz.missed_list])
    
    # Generate the whole dictionary for jinja parameters
    kwargs = {
        'jinja_branch_name': branch_name_dict[url_branch_no],
        'jinja_biz_type': business_name_dict[url_biz_type],
        'jinja_first_call': target_call_list[0][1],
        'jinja_first_counter': target_call_list[0][0],
        'jinja_second_call': target_call_list[1][1],
        'jinja_second_counter': target_call_list[1][0],
        'jinja_third_call': target_call_list[2][1],
        'jinja_third_counter': target_call_list[2][0],
        'jinja_waiting_list': html_queue_list,
        'jinja_missed_list': html_missed_list
    }
    
    # Console echo
    print(f'''
          Function: Auto Refresh for Display Screen
          Branch: {branch_name_dict[url_branch_no]}
          Business Type: {business_name_dict[url_biz_type]}
          Status: Success
          Response: None
          ''')
    return render_template('display.html', **kwargs)


"""
Routes for taking queuing number.
"""
@app.route('/www.bos.com/client/<url_branch_no>', methods = ['POST', 'GET'])
def clientSPA(url_branch_no):
    url_branch_no = url_branch_no.upper()
    
    # When clients visit our page using GET method...
    if request.method == 'GET':
        
        # Generate the whole dictionary for jinja parameters
        kwargs = {
                'jinja_branch_name':branch_name_dict[url_branch_no]
            }
        return render_template('client_queue.html', **kwargs)
    
    # When clients submit some information...
    if request.method == 'POST':
        input_email = request.form.get('input_email')
        input_biz_type = request.form.get('input_type')
        target_bank = [x for x in cache if x.branch_no == url_branch_no][0]
        target_biz = [y for y in target_bank.biz_list if y.biz_type == input_biz_type][0]
        
        # If the queue is stopped...
        if not target_biz.status:
            
            # Generate the whole dictionary for jinja parameters
            kwargs = {
                'jinja_branch_name': branch_name_dict[url_branch_no],
                'jinja_biz_type': business_name_dict[input_biz_type],
                'jinja_queue_length': len(target_biz.queue_list)
            }
            
            # Console echo
            print(f'''
                  Function: Take a new queue no
                  Branch: {branch_name_dict[url_branch_no]}
                  Business Type: {business_name_dict[input_biz_type]}
                  Status: Failure
                  Response: Queue is stopped.
                  ''')
                  
            return render_template('client_fail.html', **kwargs)
        
        # If the client successfully take the queue...
        else:
            new_queue_no = target_biz.queue_count + 1
            newNode = CusNode(input_biz_type, new_queue_no, input_email)
            target_biz.addNode(newNode)
            
            # Generate the whole dictionary for jinja parameters
            kwargs = {
                'jinja_branch_name': branch_name_dict[url_branch_no],
                'jinja_biz_type': business_name_dict[input_biz_type],
                'jinja_get_queue_no': new_queue_no
            }
            
            # Console echo
            print(f'''
                  Function: Take a new queue no
                  Branch: {branch_name_dict[url_branch_no]}
                  Business Type: {business_name_dict[input_biz_type]}
                  Status: Success
                  Response: Queue no - {new_queue_no}
                  ''')
            return render_template('client_suceed.html', **kwargs)
        

"""
Routes for cro management.
"""
@app.route('/www.bos.com/cro/<url_branch_no>', methods = ['POST', 'GET'])
def croSPA(url_branch_no):
    url_branch_no = url_branch_no.upper()
    # When cros visit our page using GET method...
    if request.method == 'GET':
        
        # Generate the whole dictionary for jinja parameters
        kwargs = {
                'jinja_branch_name':branch_name_dict[url_branch_no]
            }
        return render_template('CRO_general.html', **kwargs)

    # When cros conduct some opetations...
    if request.method == 'POST':
        input_biz_type = request.form.get('input_type')
        input_action = request.form.get('action')
        target_bank = [x for x in cache if x.branch_no == url_branch_no][0]
        target_biz = [y for y in target_bank.biz_list if y.biz_type == input_biz_type][0]
        
        # Stop queue
        if input_action == 'Stop':
            target_biz.stop()
            
            # Generate the whole dictionary for jinja parameters
            kwargs = {
                    'jinja_branch_name':branch_name_dict[url_branch_no],
                    'jinja_biz_type':business_name_dict[input_biz_type]
                }
            
            # Console echo
            print(f'''
                  Function: Stop the queue
                  Branch: {branch_name_dict[url_branch_no]}
                  Business Type: {business_name_dict[input_biz_type]}
                  Status: Success
                  Response: None
                  ''')
            return render_template('CRO_stop.html', **kwargs)

        # View queue
        elif input_action == 'View':
            
            # Generate queue list for jinja parameters
            if target_biz.queue_list == []:
                html_queue_list = "Nobody in queue."
            else:
                html_queue_list = " - ".join([str(x.queue_no) for x in target_biz.queue_list])
            
            # Generate counter information for jinja parameters
            html_counter = []
            for counter_obj in target_biz.counter_list:
                if not counter_obj.cur_serve:
                    cur_serve = "[Nobody]"
                else:
                    cur_serve = str(counter_obj.cur_serve[0].queue_no) + business_name_dict[counter_obj.cur_serve[1]]
                html_counter.append("Counter" + " " + str(counter_obj.counter_no) +" - "+ cur_serve)
            
            # Generate missed list fo jinja parameters
            if target_biz.queue_list == []:
                html_missed_list = "Nobody missed call."
            else:
                html_missed_list = " - ".join([str(x.queue_no) for x in target_biz.missed_list])
            
            # Generate the whole dictionary for jinja parameters
            kwargs = {
                    'jinja_branch_name': branch_name_dict[url_branch_no],
                    'jinja_queue_list': html_queue_list,
                    'jinja_counter_list': html_counter,
                    'jinja_missed_list': html_missed_list
                }
            
            # Console echo
            print(f'''
                  Function: View the queue
                  Branch: {branch_name_dict[url_branch_no]}
                  Business Type: {business_name_dict[input_biz_type]}
                  Status: Success
                  Response: None
                  ''')
                  
            return render_template('CRO_view.html', **kwargs)
        
        #Reinitiate queue
        elif input_action == 'Reinitiate':
            target_biz.reInitiate()
            
            # Generate the whole dictionary for jinja parameters
            kwargs = {
                    'jinja_branch_name':branch_name_dict[url_branch_no],
                    'jinja_biz_type':business_name_dict[input_biz_type]
                }
            
            print(f'''
                  Function: Reinitiate the queue
                  Branch: {branch_name_dict[url_branch_no]}
                  Business Type: {business_name_dict[input_biz_type]}
                  Status: Success
                  Response: None
                  ''')
                  
            return render_template('CRO_reinitiate.html', **kwargs)
        
        #reset queue
        elif input_action == 'Reset':
            target_biz.reset()
            
            # Generate the whole dictionary for jinja parameters
            kwargs = {
                    'jinja_branch_name':branch_name_dict[url_branch_no]
                }
            print(f'''
                  Function: Reset the queue
                  Branch: {branch_name_dict[url_branch_no]}
                  Business Type: {business_name_dict[input_biz_type]}
                  Status: Success
                  Response: None
                  ''')
                  
            return render_template('CRO_reset.html', **kwargs)

"""
Routes for counter staff.
"""
@app.route('/www.bos.com/counter/<url_branch_no>/<url_biz_type>/<url_counter_no>', methods=['POST', 'GET'])
def counterSPA(url_branch_no, url_biz_type, url_counter_no):
    url_branch_no = url_branch_no.upper()
    url_biz_type = url_biz_type.upper()
    
    # GET method, return basic page, use static params from url
    if request.method == "GET":
        kwargs = {
                    'jinja_branch_name':branch_name_dict[url_branch_no],
                    'jinja_biz_type':business_name_dict[url_biz_type],
                    'jinja_text': ""
            }
        return render_template('Counter.html', **kwargs)

    # POST method, depends on form responses to decide use dynamic or static params
    if request.method == "POST":
        target_bank = [x for x in cache if x.branch_no == url_branch_no][0]
        target_biz = [y for y in target_bank.biz_list if y.biz_type == url_biz_type][0]
        target_counter = [z for z in target_biz.counter_list if int(z.counter_no) == int(url_counter_no)][0]
        input_action = request.values.get('action')
        input_biz_type = request.form.get('input_type')

        # Call
        if input_action == "Call":
            if url_biz_type == "A":
                target_biz = [y for y in target_bank.biz_list if y.biz_type == input_biz_type][0]
                from_biz = [y for y in target_bank.biz_list if y.biz_type == url_biz_type][0]
                target_counter = [z for z in from_biz.counter_list if int(z.counter_no) == int(url_counter_no)][0]
                return_term = target_counter.callNextClient(target_biz, business_name_dict[url_biz_type])
                
                if return_term == -1:
                    msg = f"There is no more client under {business_name_dict[input_biz_type]} business type"
                    
                    # Generate the whole dictionary for jinja parameters
                    kwargs = {
                            'jinja_branch_name':branch_name_dict[url_branch_no],
                            'jinja_biz_type':business_name_dict[input_biz_type],
                            'jinja_text': msg
                    }
                    
                    print(f'''
                            Function: Call
                            Branch: {branch_name_dict[url_branch_no]}
                            Business Type: {business_name_dict[url_biz_type]}
                            Execute on Business Type: {business_name_dict[input_biz_type]}
                            Status: Failure
                            Response: No more client.
                    ''')
                    
                    return render_template('Counter.html', **kwargs)
                else:
                    msg = f"Queue No {return_term.queue_no} under {business_name_dict[input_biz_type]} is called!"
                    
                    # Generate the whole dictionary for jinja parameters
                    kwargs = {
                            'jinja_branch_name':branch_name_dict[url_branch_no],
                            'jinja_biz_type':business_name_dict[input_biz_type],
                            'jinja_text': msg
                    }
                    
                    print(f'''
                            Function: Call
                            Branch: {branch_name_dict[url_branch_no]}
                            Business Type: {business_name_dict[url_biz_type]}
                            Execute on Business Type: {business_name_dict[input_biz_type]}
                            Status: Success
                            Response: Call {business_name_dict[return_term.biz_type]} Queue No {return_term.queue_no}
                    ''')
                    
                    return render_template('Counter.html', **kwargs)
            else:
                return_term = target_counter.callNextClient(target_biz, business_name_dict[url_biz_type])
                
                if return_term == -1:
                    msg = f"There is no more client under {business_name_dict[url_biz_type]} business type"
                    
                    # Generate the whole dictionary for jinja parameters
                    kwargs = {
                            'jinja_branch_name':branch_name_dict[url_branch_no],
                            'jinja_biz_type':business_name_dict[url_biz_type],
                            'jinja_text': msg
                    }
                    
                    print(f'''
                            Function: Call
                            Branch: {branch_name_dict[url_branch_no]}
                            Business Type: {business_name_dict[url_biz_type]}
                            Execute on Business Type: {business_name_dict[url_biz_type]}
                            Status: Failure
                            Response: No more client.
                    ''')
                    
                    return render_template('Counter.html', **kwargs)
                else:
                    msg = f"Queue No {return_term.queue_no} under {business_name_dict[url_biz_type]} is called!"
                    
                    # Generate the whole dictionary for jinja parameters
                    kwargs = {
                            'jinja_branch_name':branch_name_dict[url_branch_no],
                            'jinja_biz_type':business_name_dict[url_biz_type],
                            'jinja_text': msg
                    }
                    
                    print(f'''
                            Function: Call
                            Branch: {branch_name_dict[url_branch_no]}
                            Business Type: {business_name_dict[url_biz_type]}
                            Execute on Business Type: {business_name_dict[url_biz_type]}
                            Status: Success
                            Response: Call {business_name_dict[return_term.biz_type]} Queue No {return_term.queue_no}
                    ''')
                    
                    return render_template('Counter.html', **kwargs)
                
        # Onhold
        elif input_action == "Onhold":
            if url_biz_type == "A":
                target_biz = [y for y in target_bank.biz_list if y.biz_type == url_biz_type][0]
                target_counter = [z for z in target_biz.counter_list if int(z.counter_no) == int(url_counter_no)][0]
                return_term = target_counter.holdNextClient(target_biz)
                
                if return_term == -1:
                    msg = f"There is no more client under {business_name_dict[input_biz_type]} business type"
                    
                    # Generate the whole dictionary for jinja parameters
                    kwargs = {
                            'jinja_branch_name':branch_name_dict[url_branch_no],
                            'jinja_biz_type':business_name_dict[url_biz_type],
                            'jinja_text': msg
                    }
                    
                    print(f'''
                            Function: Onhold
                            Branch: {branch_name_dict[url_branch_no]}
                            Business Type: {business_name_dict[url_biz_type]}
                            Execute on Business Type: {business_name_dict[input_biz_type]}
                            Status: Failure
                            Response: No more client.
                    ''')
                    
                    return render_template('Counter.html', **kwargs)
                else:
                    msg = f"Queue No {return_term.queue_no} under {business_name_dict[input_biz_type]} is on hold!"
                    
                    # Generate the whole dictionary for jinja parameters
                    kwargs = {
                            'jinja_branch_name':branch_name_dict[url_branch_no],
                            'jinja_biz_type':business_name_dict[url_biz_type],
                            'jinja_text': msg
                    }
                    
                    print(f'''
                            Function: Onhold
                            Branch: {branch_name_dict[url_branch_no]}
                            Business Type: {business_name_dict[url_biz_type]}
                            Execute on Business Type: {business_name_dict[input_biz_type]}
                            Status: Success
                            Response: Onhold {business_name_dict[return_term.biz_type]} Queue No {return_term.queue_no}
                    ''')
                    
                    return render_template('Counter.html', **kwargs)
            else:
                return_term = target_counter.holdNextClient(target_biz)
                
                if return_term == -1:
                    msg = f"There is no more client under {business_name_dict[url_biz_type]} business type"
                    
                    # Generate the whole dictionary for jinja parameters
                    kwargs = {
                            'jinja_branch_name':branch_name_dict[url_branch_no],
                            'jinja_biz_type':business_name_dict[url_biz_type],
                            'jinja_text': msg
                    }
                    
                    print(f'''
                            Function: Onhold
                            Branch: {branch_name_dict[url_branch_no]}
                            Business Type: {business_name_dict[url_biz_type]}
                            Execute on Business Type: {business_name_dict[url_biz_type]}
                            Status: Failure
                            Response: No more client.
                    ''')
                    
                    return render_template('Counter.html', **kwargs)
                else:
                    msg = f"Queue No {return_term.queue_no} under {business_name_dict[url_biz_type]} is on hold!"
                    
                    # Generate the whole dictionary for jinja parameters
                    kwargs = {
                            'jinja_branch_name':branch_name_dict[url_branch_no],
                            'jinja_biz_type':business_name_dict[url_biz_type],
                            'jinja_text': msg
                    }
                    
                    print(f'''
                            Function: Onhold
                            Branch: {branch_name_dict[url_branch_no]}
                            Business Type: {business_name_dict[url_biz_type]}
                            Execute on Business Type: {business_name_dict[url_biz_type]}
                            Status: Success
                            Response: Onhold {business_name_dict[return_term.biz_type]} Queue No {return_term.queue_no}
                    ''')
                    
                    return render_template('Counter.html', **kwargs)
        
        # Reschedule
        elif input_action == "Reschedule":
            
            target_biz = [y for y in target_bank.biz_list if y.biz_type == input_biz_type][0]
            target_counter = [z for z in target_biz.counter_list if int(z.counter_no) == int(url_counter_no)][0]
            input_queue_no = request.values.get('que_no')
            if input_queue_no == "":
                msg = "Invalid input detected!"
                
                # Generate the whole dictionary for jinja parameters
                kwargs = {
                        'jinja_branch_name':branch_name_dict[url_branch_no],
                        'jinja_biz_type':business_name_dict[url_biz_type],
                        'jinja_text': msg
                }
                
                print(f'''
                        Function: Reschedule
                        Branch: {branch_name_dict[url_branch_no]}
                        Business Type: {business_name_dict[url_biz_type]}
                        Execute on Business Type: {business_name_dict[input_biz_type]}
                        Status: Failure
                        Response: No input.
                ''')
                
                return render_template('Counter.html', **kwargs)
            else:
                return_term = target_counter.reschedule(input_queue_no, target_biz)
                
                msg = f"Now rescheduling Queue No {return_term.queue_no} to {business_name_dict[input_biz_type]} !"
                
                # Generate the whole dictionary for jinja parameters
                kwargs = {
                        'jinja_branch_name':branch_name_dict[url_branch_no],
                        'jinja_biz_type':business_name_dict[url_biz_type],
                        'jinja_text': msg
                }
                
                print(f'''
                        Function: Reschedule
                        Branch: {branch_name_dict[url_branch_no]}
                        Business Type: {business_name_dict[url_biz_type]}
                        Execute on Business Type: {business_name_dict[input_biz_type]}
                        Status: Success
                        Response: Reschedule {business_name_dict[return_term.biz_type]} Queue No {return_term.queue_no} 
                ''')
                
                return render_template('Counter.html', **kwargs)

if __name__ == '__main__':
    print('Loading ...')
    app.run()
    print('Terminating ...')