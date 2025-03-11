CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    action TEXT,
    rule TEXT,
    interface_in TEXT,
    ipsrc TEXT,
    ipdst TEXT,
    proto TEXT,
    portsrc FLOAT,
    portdst FLOAT,
    year INT,
    month INT,
    day INT,
    time TIME,
    portsrc_range TEXT,
    portdst_range TEXT,
    hour INT,
    ipsrc_class TEXT,
    ipdst_class TEXT,
    isprivatesrc TEXT,
    isprivatedst TEXT
);

COPY logs(date, action, rule, interface_in, ipsrc, ipdst, proto, portsrc, portdst, year, month, day, time, portsrc_range, portdst_range, hour, ipsrc_class, ipdst_class, isprivatesrc, isprivatedst)
FROM '/data/logs_processed.csv'
DELIMITER ','
CSV HEADER;
