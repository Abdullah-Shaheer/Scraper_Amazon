import random
import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent


xl = pd.read_excel("ASINS Scraping - Stage 1.xlsx")
asins = xl["ASIN"].tolist()


async def fetch_asin_data(session, asin):
    url = f"https://www.amazon.co.uk/dp/{asin}"
    ua = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    ]
    # You can use ua or ua1 both here I am using ua1
    ua1 = UserAgent()
    headers = {
        'User-Agent': ua1.random,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                print(f"Fetched data for ASIN: {asin}")
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')

                title = None
                try:
                    title = soup.find("span", {'id': 'productTitle'}).text.strip()
                    if not title:
                        title = soup.find("span", {'class': 'a-size-large product-title-word-break'}).text.strip()
                except:
                    print(f"Unable to fetch title for ASIN: {asin}")

                photo = None
                try:
                    product_photo_element = soup.find("div", {'class': 'imgTagWrapper'})
                    if product_photo_element:
                        photo_element = product_photo_element.find("img")
                        if photo_element:
                            photo = photo_element.get("src")
                        else:
                            print(f"No image found inside 'imgTagWrapper' for ASIN: {asin}")
                    else:
                        product_photo_element = soup.find("div", {'id': 'imgTagWrapperId'})
                        photo_element = product_photo_element.find("img")
                        if photo_element:
                            photo = photo_element.get("src")
                except Exception as e:
                    print(f"Error while fetching product image for ASIN: {asin}, Error: {e}")

                try:
                    about_this_item_details = []

                    about_ = soup.find("div", {'id': 'feature-bullets'})

                    if about_:
                        ul = about_.find("ul", class_="a-unordered-list a-vertical a-spacing-mini")
                        table = soup.find("table")

                        if table:
                            rows = table.find_all("tr")
                            for row in rows:
                                cells = row.find_all("td")
                                if len(cells) == 2:
                                    key = cells[0].get_text(strip=True)
                                    value = cells[1].get_text(strip=True)
                                    about_this_item_details.append(f"{key}: {value}")

                        if ul:
                            list_items = ul.find_all("li", class_="a-spacing-mini")
                            for item in list_items:
                                al = item.find("span", class_="a-list-item")
                                if al:
                                    about_this_item_details.append(al.text.strip())
                    about_this_item_details = [detail.replace("See more", "").strip() for detail in
                                               about_this_item_details]

                except Exception as e:
                    print(f"Error while fetching product details, Error: {e}")

                description = None
                try:
                    description_div = soup.find("div", {'id': 'productDescription'})
                    if description_div:
                        structured_description = []
                        for element in description_div.find_all(True):
                            if element.name == 'p':
                                # Handle paragraphs
                                text = element.get_text(strip=True)
                                if text:
                                    structured_description.append(f"{text}")

                            elif element.name in ['h1', 'h2', 'h3']:
                                heading = element.get_text(strip=True)
                                structured_description.append(f"{heading}")

                            elif element.name == 'table':
                                structured_description.append(f"\n{str(element)}")

                            elif element.name == 'ul':
                                list_items = [f"- {li.get_text(strip=True)}" for li in element.find_all('li')]
                                if list_items:
                                    structured_description.append("\n" + "\n".join(list_items))
                        description = "\n\n".join(structured_description)

                        description = description.replace("See more", "").strip()

                    else:
                        description_div = soup.find("div", {'class': 'a-section a-spacing-small'})
                        if description_div:
                            structured_description = []
                            for element in description_div.find_all(True):
                                if element.name == 'p':
                                    text = element.get_text(strip=True)
                                    if text:
                                        structured_description.append(f"{text}")

                                elif element.name in ['h1', 'h2', 'h3']:
                                    heading = element.get_text(strip=True)
                                    structured_description.append(f"{heading}")

                                elif element.name == 'table':
                                    structured_description.append(f"\n{str(element)}")

                                elif element.name == 'ul':
                                    list_items = [f"- {li.get_text(strip=True)}" for li in element.find_all('li')]
                                    if list_items:
                                        structured_description.append("\n" + "\n".join(list_items))

                            description = "\n\n".join(structured_description)
                            description = description.replace("See more", "").strip()

                except Exception as e:
                    print(f"Error while fetching product description from ASIN {asin} Error: {e}")
                special_ingredients = None
                general_ingredients = None

                try:
                    table = soup.find('table')
                    if table:
                        rows = table.find_all('tr')
                        for row in rows:
                            heading_td = row.find('td')
                            if heading_td and (
                                    "special ingredients" in heading_td.text.lower() or "active ingredients" in heading_td.text.lower() or
                                    "material" in heading_td.text.lower() or "material feature" in heading_td.text.lower()):
                                special_ingredients_td = row.find('td', {
                                    'class': 'a-span9'})
                                if special_ingredients_td:
                                    special_ingredients = special_ingredients_td.text.strip()
                                break
                except Exception as e:
                    pass

                if not special_ingredients:
                    try:
                        important_info = soup.find('div', {'class': 'a-section a-spacing-extra-large bucket'})

                        if important_info:
                            sections = important_info.find_all('div')
                            for section in sections:
                                span = section.find('span')
                                if span and 'Ingredients:' in span.text:
                                    p_tags = section.find_all('p')
                                    for p_tag in p_tags:
                                        if p_tag and p_tag.get_text(strip=True):
                                            general_ingredients = p_tag.get_text(strip=True)
                                            break
                                htag = section.find('h4')
                                if htag and 'Ingredients:' in htag.text:
                                    p_tags = section.find_all('p')
                                    for p_tag in p_tags:
                                        if p_tag and p_tag.get_text(strip=True):
                                            general_ingredients = p_tag.get_text(strip=True)
                                            break

                        if not general_ingredients:
                            general_ingredients = "Ingredients information not available"
                    except Exception as e:
                        pass

                final_ingredients = special_ingredients if special_ingredients else general_ingredients
                if not final_ingredients:
                    final_ingredients = "Ingredients information not available"

                special_feature = None
                try:
                    table = soup.find('table')
                    if table:
                        rows = table.find_all('tr')
                        for row in rows:
                            heading_td = row.find('td')
                            if heading_td and (
                                    "special feature" in heading_td.text.lower() or "special features" in heading_td.text.lower()):
                                special_features_td = row.find('td', {
                                    'class': 'a-span9'})
                                if special_features_td:
                                    special_feature = special_features_td.text.strip()
                                break
                    if not special_feature:
                        tech_table = soup.find("table", {'id': 'productDetails_techSpec_section_1'})
                        rows = tech_table.find_all('tr')
                        for row in rows:
                            heading_td = row.find('th', {'class': 'a-color-secondary a-size-base prodDetSectionEntry'})
                            if heading_td and (
                                    "special feature" in heading_td.text.lower() or "special features" in heading_td.text.lower()):
                                special_features_td = row.find('td', {
                                    'class': 'a-size-base prodDetAttrValue'})
                                if special_features_td:
                                    special_feature = special_features_td.text.strip()
                                break

                except Exception as e:
                    pass

                return {"ASIN": asin,
                        "Product Photo": photo,
                        "Product Title": title,
                        "About This Item": "\n".join(about_this_item_details),
                        "Special Ingredients": final_ingredients,
                        "Special Feature": special_feature,
                        "Product Description": description}
            elif response.status == 404:
                print(f"404 Error for ASIN: {asin}, skipping...")
                return None
            elif response.status == 500:
                print(f"500 status code... try using a useragent")
                return None
            else:
                print(f"Failed to fetch data for ASIN: {asin}, Status: {response.status}")
                return {"ASIN": asin, "Error": f"Status Code: {response.status}"}

    except Exception as e:
        print(f"Exception while fetching ASIN: {asin}, Error: {str(e)}")
        return {"ASIN": asin, "Error": str(e)}

async def fetch_all_asins(asins, max_concurrent=100):
    connector = aiohttp.TCPConnector(limit_per_host=max_concurrent)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_asin_data(session, asin) for asin in asins]
        results = await asyncio.gather(*tasks)

    filtered_results = [result for result in results if result is not None]
    return filtered_results


if __name__ == "__main__":
    asins_sample = asins[720:800]
    results = asyncio.run(fetch_all_asins(asins_sample, max_concurrent=50))
    df_results = pd.DataFrame(results)
    print(df_results)
    df_results.to_excel('output_asin_data_14.xlsx', index=False)

