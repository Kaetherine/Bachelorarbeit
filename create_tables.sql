CREATE TABLE color_names (
    color_code TEXT,
    color_name TEXT,
    PRIMARY KEY (color_code)
);

CREATE TABLE hex_colors (
    hex TEXT,
    rgb_r INTEGER,
    rgb_g INTEGER,
    rgb_b INTEGER,
    lab_l REAL,
    lab_a REAL,
    lab_b REAL,
    cmyk TEXT,
    color_code TEXT,
    PRIMARY KEY (hex),
    FOREIGN KEY (color_code) REFERENCES color_names (color_code)
);

CREATE TABLE products (
    retrieved_on DATE,
    source TEXT,
    product_id TEXT,
    product_name TEXT,
    price NUMERIC,
    currency TEXT,
    publish_date DATE,
    color_hex_code TEXT,
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
    PRIMARY KEY (retrieved_on, source, product_id, material_part, percent, material)
    FOREIGN KEY (retrieved_on, source, product_id) REFERENCES products (retrieved_on, source, product_id)
);

CREATE TABLE origins (
    retrieved_on DATE,
    source TEXT,
    product_id TEXT,
    country_of_origin TEXT,
    PRIMARY KEY (retrieved_on, source, product_id, country_of_origin)
    FOREIGN KEY (retrieved_on, source, product_id) REFERENCES products (retrieved_on, source, product_id)
);

CREATE TABLE related_products (
    source TEXT,
    product_id TEXT,
    related_product_id TEXT,
    PRIMARY KEY (source, product_id , related_product_id),
    FOREIGN KEY (source, product_id) REFERENCES products (source, product_id)
);

CREATE TABLE target_group_categories (
    source TEXT,
    target_group TEXT,
    category_id TEXT,
    PRIMARY KEY (source, target_group , category_id),
    FOREIGN KEY (source, target_group) REFERENCES target_groups(source, target_group_id)
);

CREATE TABLE products_by_category (
    source TEXT,
    category_id TEXT,
    product_id TEXT,
    PRIMARY KEY (source, category_id , product_id),
    FOREIGN KEY (source, category_id) REFERENCES categories(source, category_id)
);

CREATE TABLE availability (
    retrieved_on DATE,
    source TEXT,
    product_id TEXT,
    availability_status TEXT,
    PRIMARY KEY (retrieved_on, source, product_id),
    FOREIGN KEY (retrieved_on, source, product_id) REFERENCES products (retrieved_on, source, product_id)
);

CREATE TABLE color_interpretations (
    hex TEXT,
    interpret_zara_com_de TEXT,
    PRIMARY KEY (hex, interpret_zara_com_de),
    FOREIGN KEY (hex) REFERENCES hex_colors(hex)
);