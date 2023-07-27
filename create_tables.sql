CREATE TABLE color_names (
    color_code TEXT,
    color_name TEXT,
    PRIMARY KEY (color_code)
);

CREATE TABLE hex_colors (
    hex_color TEXT,
    rgb_r TEXT,
    rgb_g TEXT,
    rgb_b TEXT,
    lab_l NUMERIC,
    lab_a NUMERIC,
    lab_b NUMERIC,
    cmyk TEXT,
    color_code TEXT,
    PRIMARY KEY (hex_color),
    FOREIGN KEY (color_code) REFERENCES color_names (color_code)
);

CREATE TABLE products (
    retrieved_on DATE,
    src TEXT,
    product_id TEXT,
    product_name TEXT,
    price NUMERIC,
    currency TEXT,
    publish_date DATE,
    hex_color TEXT,
    PRIMARY KEY (retrieved_on, src, product_id),
    FOREIGN KEY (hex_color) REFERENCES hex_colors (hex_color)
);

CREATE TABLE target_groups (
    src TEXT,
    target_group_id TEXT,
    target_group TEXT,
    PRIMARY KEY (src, target_group_id)
);

CREATE TABLE categories (
    src TEXT,
    category_id TEXT,
    category_name TEXT,
    age_range TEXT,
    PRIMARY KEY (src, category_id)
);

CREATE TABLE materials (
    retrieved_on DATE,
    src TEXT,
    product_id TEXT,
    material_part TEXT,
    perc FLOAT,
    material TEXT,
    PRIMARY KEY (retrieved_on, src, product_id, material_part, perc, material),
    FOREIGN KEY (retrieved_on, src, product_id) REFERENCES products (retrieved_on, src, product_id)
);

CREATE TABLE origins (
    retrieved_on DATE,
    src TEXT,
    product_id TEXT,
    country_of_origin TEXT,
    PRIMARY KEY (retrieved_on, src, product_id, country_of_origin),
    FOREIGN KEY (retrieved_on, src, product_id) REFERENCES products (retrieved_on, src, product_id)
);

CREATE TABLE related_products (
    src TEXT,
    product_id TEXT,
    related_product_id TEXT,
    PRIMARY KEY (src, product_id , related_product_id)
);

CREATE TABLE categories_by_target_groups (
    src TEXT,
    target_group_id TEXT,
    category_id TEXT,
    PRIMARY KEY (src, target_group_id , category_id),
    FOREIGN KEY (src, target_group_id) REFERENCES target_groups (src, target_group_id)
);

CREATE TABLE products_by_categories (
    src TEXT,
    category_id TEXT,
    product_id TEXT,
    PRIMARY KEY (src, category_id , product_id),
    FOREIGN KEY (src, category_id) REFERENCES categories(src, category_id)
);

CREATE TABLE availability (
    retrieved_on DATE,
    src TEXT,
    product_id TEXT,
    availability_status TEXT,
    PRIMARY KEY (retrieved_on, src, product_id),
    FOREIGN KEY (retrieved_on, src, product_id) REFERENCES products (retrieved_on, src, product_id)
);

CREATE TABLE color_interpretations (
    hex_color TEXT,
    interpret_zara_com_de TEXT,
    PRIMARY KEY (hex_color, interpret_zara_com_de),
    FOREIGN KEY (hex_color) REFERENCES hex_colors(hex_color)
);
