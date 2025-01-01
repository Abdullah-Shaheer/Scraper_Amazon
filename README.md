# Amazon Product Scraper  

This project was designed to scrape detailed product information from Amazon using a provided list of ASINs (Amazon Standard Identification Numbers). The scraped data helped the client gain valuable insights into their target products.  

---

## 🚀 Project Overview  
- **Client Input:** An Excel file containing a list of ASINs.  
- **Objective:** Scrape product details like title, price, rating, reviews, and availability.  
- **Outcome:** Successfully delivered accurate and complete data. The client was highly satisfied with the results.  

---

## 🛠️ Technologies Used  
- **Programming Language:** Python 🐍  
- **Libraries & Tools:**  
  - `asyncio` & `aiohttp`: For asynchronous requests.  
  - `requests`: To make efficient HTTP requests.  
  - `pandas`: To handle and process the Excel file.  
  - `openpyxl`: For working with Excel data.  
  - `json`: For data storage and manipulation.  

---

## ⚙️ Features  
- **Asynchronous Scraping:** Enhanced performance by using Python's `asyncio` for concurrent requests.  
- **Error Handling:** Built-in mechanisms to retry failed requests and handle Amazon's anti-bot measures.  
- **Data Validation:** Ensured data integrity by verifying each scraped field.  
- **Customizable Output:** Delivered the final data in the desired format (Excel, CSV, JSON).  

---

## 📊 Data Fields Scraped  
The following product details were scraped:  
- **Product Title**  
- **Price**  
- **Ratings**  
- **Number of Reviews**  
- **Availability**  
- **Product Description**  
- **Category**  

---

## 📝 Steps Followed  
1. **Input Handling:** Loaded ASINs from the Excel file using `pandas`.  
2. **Asynchronous Requests:** Sent multiple requests concurrently using `aiohttp`.  
3. **Data Extraction:** Parsed the HTML responses to extract product details.  
4. **Data Cleaning:** Validated and cleaned the scraped data for accuracy.  
5. **Output:** Exported the processed data back to an Excel file.  

---

## 🏆 Client Feedback  
- **Result:** Data delivered on time with 100% accuracy.  
- **Client’s Reaction:** *"Amazing work! The scraper performed exactly as expected, and the data was perfect for our needs."*  

---

## 📂 File Structure  
- `main.py`: Core script for scraping product data.  
- `ASINs Scraping - Stage 1.xlsx`: Input file containing ASINs.  
- `amazon_details.xlsx`: Final output with scraped product details.    

---

## 💬 Connect with Me  
If you have a similar project or need custom scraping solutions, feel free to reach out!  
📧 Email: abdullahshaheer17398@gmail.com  
🌐 GitHub: [Abdullah Shaheer](https://github.com/Abdullah-Shaheer)
