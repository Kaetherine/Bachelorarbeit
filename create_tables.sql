CREATE TABLE products (
    retrieved_on DATE,
    source TEXT,
    product_id TEXT,
    product_name TEXT,
    price NUMERIC,
    currency TEXT,
    publish_date DATE,
    color_hex_code TEXT,
    color_interpretation TEXT,
    PRIMARY KEY (retrieved_on, source, product_id)
);

CREATE TABLE target_groups (
    retrieved_on DATE,
    source TEXT,
    target_group_id TEXT,
    target_group TEXT,
    PRIMARY KEY (retrieved_on, source, target_group_id)
);

CREATE TABLE categories (
    retrieved_on DATE,
    source TEXT,
    category_id TEXT,
    category_name TEXT,
    age_range TEXT,
    PRIMARY KEY (retrieved_on, source, category_id)
);

CREATE TABLE materials (
    retrieved_on DATE,
    source TEXT,
    product_id TEXT,
    material_part TEXT,
    percent FLOAT,
    material TEXT,
    FOREIGN KEY (retrieved_on, source, product_id) REFERENCES products (retrieved_on, source, product_id)
);

CREATE TABLE origins (
    retrieved_on DATE,
    source TEXT,
    product_id TEXT,
    country_of_origin TEXT,
    FOREIGN KEY (retrieved_on, source, product_id) REFERENCES products (retrieved_on, source, product_id)
);

CREATE TABLE related_products (
    source TEXT,
    product_id TEXT,
    related_product_id TEXT,
    FOREIGN KEY (source, product_id) REFERENCES products (source, product_id)
);

CREATE TABLE target_group_categories (
    source TEXT,
    target_group TEXT,
    category_id TEXT,
    FOREIGN KEY (source, target_group) REFERENCES target_groups(source, target_group_id)
);

CREATE TABLE category_products (
    source TEXT,
    category_id TEXT,
    product_id TEXT,
    FOREIGN KEY (source, category_id) REFERENCES categories(source, category_id)
);

CREATE TABLE availability (
    retrieved_on DATE,
    source TEXT,
    product_id TEXT,
    availability_status TEXT,
    FOREIGN KEY (source, category_id) REFERENCES categories(source, category_id)
);

CREATE TABLE color_codes (
    color_hex_code TEXT,
    source TEXT,
    FOREIGN KEY (source, category_id) REFERENCES categories(source, category_id)
);
