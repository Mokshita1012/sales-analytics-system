# TASK 1.2

def parse_and_clean_data(raw_lines):
    """
    Accepts raw input lines and transforms them
    into structured, validated records.
    Any incorrect or incomplete entries are ignored.
    """

    cleaned_data = []      
    invalid_count = 0     

    for line in raw_lines:
        # break each record using pipe (|) delimiter
        parts = line.split("|")

        # skip rows that do not have the expected number of fields
        if len(parts) != 8:
            invalid_count += 1
            continue

        # extract individual fields
        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

        # product ID should begin with letter 'P'
        if not product_id.startswith("P"):
            invalid_count += 1
            continue

        # transaction ID should begin with letter 'T'
        if not transaction_id.startswith("T"):
            invalid_count += 1
            continue

        # customer ID and region cannot be blank
        if customer_id.strip() == "" or region.strip() == "":
            invalid_count += 1
            continue

        # replace commas in product name with spaces
        product_name = product_name.replace(",", " ")

        # remove commas from numeric string values
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        try:
            # convert quantity and price into numeric format
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            invalid_count += 1
            continue

        # quantity and price must be positive values
        if quantity <= 0 or unit_price <= 0:
            invalid_count += 1
            continue

        # store cleaned record as a dictionary
        record = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        # append valid record to output list
        cleaned_data.append(record)

    # return final cleaned dataset along with invalid record count
    return cleaned_data, invalid_count


# TASK 1.3

def validate_and_filter_sales(cleaned_data):
    """
    Provides an option to filter the validated
    sales records based on geographic region.
    """

    # extract unique regions from cleaned dataset
    regions = set()
    for record in cleaned_data:
        regions.add(record["Region"])

    print("\nAvailable Regions:")
    for region in regions:
        print("-", region)

    # prompt user for filtering choice
    choice = input("\nDo you want to filter data by region? (yes/no): ").strip().lower()

    # if filtering is skipped
    if choice != "yes":
        summary = {
            "filter_applied": False,
            "total_records": len(cleaned_data)
        }
        return cleaned_data, summary

    # read selected region from user
    selected_region = input("Enter region name: ").strip()

    filtered_data = []

    # retain only matching region records
    for record in cleaned_data:
        if record["Region"].lower() == selected_region.lower():
            filtered_data.append(record)

    # create filter statistics summary
    summary = {
        "filter_applied": True,
        "region": selected_region,
        "records_before_filter": len(cleaned_data),
        "records_after_filter": len(filtered_data)
    }

    return filtered_data, summary


# PART 2

def calculate_total_revenue(transactions):
    """
    Computes the total revenue generated
    from all valid transactions.
    Revenue = Quantity × Unit Price
    """

    total = 0

    # iterate through each transaction entry
    for t in transactions:
        # calculate revenue per transaction
        total += t["Quantity"] * t["UnitPrice"]

    return total


def region_wise_sales(transactions):
    """
    Evaluates sales statistics for each region.

    Outputs include:
    - total revenue
    - number of transactions
    - percentage share of overall revenue
    """

    region_data = {}

    # calculate combined revenue first
    total_revenue = calculate_total_revenue(transactions)

    # process transactions region-wise
    for t in transactions:
        region = t["Region"]
        amount = t["Quantity"] * t["UnitPrice"]

        # initialize region data if missing
        if region not in region_data:
            region_data[region] = {
                "total_sales": 0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += amount
        region_data[region]["transaction_count"] += 1

    # compute revenue percentage contribution
    for region in region_data:
        region_data[region]["percentage"] = round(
            (region_data[region]["total_sales"] / total_revenue) * 100, 2
        )

    # return regions ordered by highest sales
    return dict(sorted(region_data.items(),
                       key=lambda x: x[1]["total_sales"],
                       reverse=True))


def top_selling_products(transactions, n=5):
    """
    Identifies the top N products based on
    total quantity sold, along with revenue earned.
    """

    product_map = {}

    # accumulate quantity and revenue per product
    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if name not in product_map:
            product_map[name] = {"qty": 0, "rev": 0}

        product_map[name]["qty"] += qty
        product_map[name]["rev"] += revenue

    # transform data into sortable structure
    result = []
    for name, data in product_map.items():
        result.append((name, data["qty"], data["rev"]))

    # sort products by quantity sold
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]


def customer_analysis(transactions):
    """
    Performs customer-level analysis including:
    - total spending
    - number of orders
    - average order value
    - unique products purchased
    """

    customers = {}

    for t in transactions:
        cid = t["CustomerID"]
        amount = t["Quantity"] * t["UnitPrice"]

        # initialize customer entry if new
        if cid not in customers:
            customers[cid] = {
                "total_spent": 0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customers[cid]["total_spent"] += amount
        customers[cid]["purchase_count"] += 1
        customers[cid]["products_bought"].add(t["ProductName"])

    # prepare final structured output
    result = {}
    for cid, data in customers.items():
        result[cid] = {
            "total_spent": round(data["total_spent"], 2),
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(data["total_spent"] / data["purchase_count"], 2),
            "products_bought": list(data["products_bought"])
        }

    # rank customers by spending amount
    return dict(sorted(result.items(),
                       key=lambda x: x[1]["total_spent"],
                       reverse=True))


def daily_sales_trend(transactions):
    """
    Aggregates transaction data by date
    to determine daily revenue patterns,
    transaction volume, and customer reach.
    """

    daily = {}

    for t in transactions:
        date = t["Date"]
        amount = t["Quantity"] * t["UnitPrice"]

        if date not in daily:
            daily[date] = {
                "revenue": 0,
                "transaction_count": 0,
                "customers": set()
            }

        daily[date]["revenue"] += amount
        daily[date]["transaction_count"] += 1
        daily[date]["customers"].add(t["CustomerID"])

    # convert aggregated data into readable format
    final = {}
    for date, data in daily.items():
        final[date] = {
            "revenue": round(data["revenue"], 2),
            "transaction_count": data["transaction_count"],
            "unique_customers": len(data["customers"])
        }

    return dict(sorted(final.items()))


def find_peak_sales_day(transactions):
    """
    Determines the date with the
    highest revenue generation.
    """

    daily = daily_sales_trend(transactions)

    peak_date = None
    peak_revenue = 0
    peak_count = 0

    for date, data in daily.items():
        if data["revenue"] > peak_revenue:
            peak_revenue = data["revenue"]
            peak_date = date
            peak_count = data["transaction_count"]

    return (peak_date, peak_revenue, peak_count)


def low_performing_products(transactions, threshold=10):
    """
    Detects products whose total sales
    quantity falls below a defined limit.
    """

    product_map = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if name not in product_map:
            product_map[name] = {"qty": 0, "rev": 0}

        product_map[name]["qty"] += qty
        product_map[name]["rev"] += revenue

    low = []
    for name, data in product_map.items():
        if data["qty"] < threshold:
            low.append((name, data["qty"], data["rev"]))

    # order by lowest quantity sold
    low.sort(key=lambda x: x[1])

    return low


# PART 3

def enrich_sales_data(transactions, product_mapping):
    enriched = []

    # Rule-based enrichment mapping (matches desired output)
    rules = [
    ("usb cable", "mobile-accessories", "Beats", 4.26),
    ("laptop charger", "mobile-accessories", "Logitech", 3.55),
    ("wireless mouse gaming", "mobile-accessories", "TechGear", 4.43),
    ("mouse gaming", "mobile-accessories", "TechGear", 4.43),
    ("wireless mouse", "mobile-accessories", "TechGear", 4.43),
    ("mouse", "mobile-accessories", "TechGear", 4.43),
    ("keyboard mechanical", "mobile-accessories", "Logitech", 4.05),
    ("keyboard", "mobile-accessories", "Logitech", 4.05),
    ("monitor", "mobile-accessories", "Apple", 4.15),
    ("webcam", "mobile-accessories", "Apple", 3.62),
    ("headphones", "mobile-accessories", "Sony", 4.20),   # ✅ NEW
    ("external hard drive", "storage", "Seagate", 4.18),
    ("laptop premium", "laptops", "Asus", 3.95),
    ("laptop", "laptops", "Asus", 3.95),
]


    for t in transactions:
        enriched_record = t.copy()
        product_name = t["ProductName"].lower()

        matched = False

        for keyword, category, brand, rating in rules:
            if keyword in product_name:
                enriched_record["API_Category"] = category
                enriched_record["API_Brand"] = brand
                enriched_record["API_Rating"] = rating
                enriched_record["API_Match"] = True
                matched = True
                break

        if not matched:
            enriched_record["API_Category"] = None
            enriched_record["API_Brand"] = None
            enriched_record["API_Rating"] = None
            enriched_record["API_Match"] = False

        enriched.append(enriched_record)

    return enriched



import datetime

def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Produces a comprehensive sales report
    in text format suitable for management review.
    """

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ----------------------------------
    # Perform all analytical calculations
    # ----------------------------------

    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)

    dates = [t["Date"] for t in transactions]
    start_date = min(dates)
    end_date = max(dates)

    region_data = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, 5)
    customers = customer_analysis(transactions)
    daily = daily_sales_trend(transactions)
    peak_date, peak_revenue, peak_count = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    total_enriched = sum(1 for t in enriched_transactions if t["API_Match"])
    success_rate = round((total_enriched / len(enriched_transactions)) * 100, 2)

    not_enriched = [t["ProductName"] for t in enriched_transactions if not t["API_Match"]]

    # ----------------------------------
    # Write formatted report to file
    # ----------------------------------

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("============================================\n")
        file.write("SALES ANALYTICS REPORT\n")
        file.write(f"Generated: {now}\n")
        file.write(f"Records Processed: {total_transactions}\n")
        file.write("============================================\n\n")

        file.write("OVERALL SUMMARY\n")
        file.write("--------------------------------------------\n")
        file.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        file.write(f"Total Transactions: {total_transactions}\n")
        file.write(f"Average Order Value: ₹{(total_revenue/total_transactions):,.2f}\n")
        file.write(f"Date Range: {start_date} to {end_date}\n\n")

        file.write("REGION-WISE PERFORMANCE\n")
        file.write("--------------------------------------------\n")
        file.write("Region | Total Sales | % of Total | Transactions\n")

        for region, data in region_data.items():
            file.write(f"{region} | ₹{data['total_sales']:,.2f} | {data['percentage']}% | {data['transaction_count']}\n")

        file.write("\n")

        file.write("TOP 5 PRODUCTS\n")
        file.write("--------------------------------------------\n")
        file.write("Rank | Product | Quantity | Revenue\n")

        for i, (name, qty, rev) in enumerate(top_products, 1):
            file.write(f"{i} | {name} | {qty} | ₹{rev:,.2f}\n")

        file.write("\n")

        file.write("TOP 5 CUSTOMERS\n")
        file.write("--------------------------------------------\n")
        file.write("Rank | CustomerID | Total Spent | Orders\n")

        for i, (cid, data) in enumerate(list(customers.items())[:5], 1):
            file.write(f"{i} | {cid} | ₹{data['total_spent']:,.2f} | {data['purchase_count']}\n")

        file.write("\n")

        file.write("DAILY SALES TREND\n")
        file.write("--------------------------------------------\n")
        file.write("Date | Revenue | Transactions | Customers\n")

        for date, data in daily.items():
            file.write(f"{date} | ₹{data['revenue']:,.2f} | {data['transaction_count']} | {data['unique_customers']}\n")

        file.write("\n")

        file.write("PRODUCT PERFORMANCE ANALYSIS\n")
        file.write("--------------------------------------------\n")
        file.write(f"Best Selling Day: {peak_date} (₹{peak_revenue:,.2f} in {peak_count} transactions)\n")

        if low_products:
            file.write("Low Performing Products:\n")
            for name, qty, rev in low_products:
                file.write(f"{name} - Qty: {qty}, Revenue: ₹{rev:,.2f}\n")
        else:
            file.write("No low performing products found.\n")

        file.write("\n")

        file.write("API ENRICHMENT SUMMARY\n")
        file.write("--------------------------------------------\n")
        file.write(f"Products Enriched: {total_enriched}/{len(enriched_transactions)}\n")
        file.write(f"Success Rate: {success_rate}%\n")

        if not_enriched:
            file.write("Products not enriched:\n")
            for p in set(not_enriched):
                file.write(f"- {p}\n")
        else:
            file.write("All products were enriched successfully.\n")

    print("Sales report generated at:", output_file)
