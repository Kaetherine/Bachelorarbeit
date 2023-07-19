import get_zara as zara

category_ids = zara.get_categories()
print(category_ids)

#%%
print(category_ids[:2])

# %%
products_by_category = zara.get_product_list(category_ids[3:5])

#%%
print(products_by_category)
print(len(products_by_category))

# %%
product_ids = zara.get_product_ids(products_by_category)
print(product_ids)

# %%
product_details = zara.get_product_details(product_ids[3:5])

#%%
print(product_details)
print(len(product_details))

# %%
related_products = zara.get_related_products(product_ids[3:5])

#%%
print(related_products)