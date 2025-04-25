import csv
import random
import time

def generate_data(filename="website_traffic.csv", num_rows=100):
    pages = ["/home", "/products", "/cart", "/checkout", "/blog"]
    devices = ["mobile", "desktop", "tablet"]
    countries = ["US", "IN", "UK", "DE", "AU"]
    browsers = ["Chrome", "Firefox", "Safari", "Edge", "Opera"]

    current_time = int(time.time() * 1000)
    past_time = current_time - (7 * 24 * 60 * 60 * 1000)  

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["user_id", "page", "device", "country", "browser", "timestamp"])

        for _ in range(num_rows):
            writer.writerow([
                f"user_{random.randint(1000, 9999)}",
                random.choice(pages),
                random.choice(devices),
                random.choice(countries),
                random.choice(browsers),
                random.randint(past_time, current_time)
            ])

    print(f"Created {filename} with {num_rows} rows.")

if __name__ == "__main__":
    generate_data()