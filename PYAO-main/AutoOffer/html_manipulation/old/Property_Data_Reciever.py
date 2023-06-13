import socket, pickle, asyncio, threading, traceback
from bs4 import BeautifulSoup
from HTML import HTML
from HTML_ACTIONS import click, innerHTML_Drill
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize HTML class
html = HTML()

# Define pickle file path for storing mls data
pkl_file_path = r'C:\Users\charl\Desktop\AutoOffer\AutoOffer\html_manipulation\prop_dict.pkl'

# chromeDriverPath = r'C:\Program Files (x86)\chromedriver.exe'
# browser = webdriver.Chrome(executable_path=chromeDriverPath)  


    # Create a socket serverb
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_address = ('localhost', 5000)  # Replace with the appropriate server address
    server_socket.bind(server_address)

    # Make a que of 1 connects
    server_socket.listen(1)

    # Global flag to indicate server availability
    server_available = True

    print('Receiver program listening for connections...')

    # Function to handle client requests
    def handle_client(connection):
        
        global server_available
        while True:
            # Receive data from the property program
            received_data = connection.recv(4024)
            if not received_data:
                break

            
            if server_available:
                server_available = False

                # Deserialize the received data using pickle
                deserialized_data = pickle.loads(received_data)

                # Read pickle file
                with open(pkl_file_path, 'rb') as read_file:
                    try:
                        old_deserialized_data = pickle.load(read_file)
                    
                    # Catch error if pkl file contains no pickiled data
                    except EOFError:
                        old_deserialized_data = {}
                        print(f"Pickle does not contain pickled data: {old_deserialized_data}")


                # Overwrite pickle file
                with open(pkl_file_path, 'wb') as write_file:

                    # Get only the new properties added
                    new_deserialized_data = {key: value for key,value in deserialized_data.items() if key not in old_deserialized_data}

                    # Update dictionary with new listings
                    updated_deserialized_data = old_deserialized_data.copy()
                    updated_deserialized_data.update(new_deserialized_data)

                    # Update the pickle file with new data
                    pickle.dump(updated_deserialized_data, write_file)


                print(f"Updated Data: {updated_deserialized_data}")

                # for key, value in updated_deserialized_data.items():
                #     # print(f"Paseed Key Data: {value['Street Address']}")

                try:
                    # Run asyc code on new entries only
                    # asyncio.run(main(html.webaddress['ARV'], new_deserialized_data))
                    pass
                
                # Handle all errors so Server connection doesn't stall
                except Exception:

                    # Print out the traceback information for error
                    traceback.print_exc()


                response = ("READY", {'request_wait': None})
                server_available = True
            else: 
                # If server is busy send "BUSY" response and wait 60 secods before next request
                response = ("BUSY", {'request_wait': 60})

            # Pickle the response
            pickle_data = pickle.dumps(response)

            connection.send(pickle_data)
   


    # Function to accept incoming connections
    def accept_connections(socket):

        # While loop keeps socket open to accept connections
        while True:
            # Accept incoming client connection
            connection, addr = socket.accept()

            # Print a message indicating a new connection from the client's address
            print(f"New connection from: {addr}")

            # Create a new thread to handle client communication
            client_thread = threading.Thread(target=handle_client, args=(connection,))
            
            # Start the client thread to handle communication with the client
            client_thread.start()

    # Start accepting connections in a separate thread
    accept_thread = threading.Thread(target=accept_connections(server_socket))
    accept_thread.start()




