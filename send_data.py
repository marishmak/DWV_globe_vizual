import requests
import pandas as pd

def send_data_to_server(file_path, server_url):
    try:
        # Load the CSV file
        df = pd.read_csv(file_path)
        
        # Sort by timestamp to simulate real-time data
        df = df.sort_values(by='Timestamp')
        
        # Send each package to the Flask server
        for _, row in df.iterrows():
            package = {
                "ip_address": row["ip address"],
                "Latitude": row["Latitude"],
                "Longitude": row["Longitude"],
                "Timestamp": row["Timestamp"],
                "suspicious": row["suspicious"]
            }
            
            try:
                response = requests.post(server_url, json=package)
                if response.status_code == 200:
                    print(f"Sent package: {package}")
                else:
                    print(f"Failed to send package: {response.status_code}")
            except Exception as e:
                print(f"Error occurred while sending data: {e}")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    csv_file_path = "ip_addresses.csv"
    flask_server_url = "http://flask-server:5050/receive_data"
    send_data_to_server(csv_file_path, flask_server_url)