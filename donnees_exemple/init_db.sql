CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    ipsrc TEXT,
    ipdst TEXT,
    proto TEXT,
    portsrc FLOAT,
    portdst FLOAT,
    regle FLOAT,
    action TEXT,
    interface_in TEXT,
    interface_out TEXT,
    divers FLOAT
);

COPY logs(date, ipsrc, ipdst, proto, portsrc, portdst, regle, action, interface_in, interface_out, divers)
FROM '/data/log_export.csv'
DELIMITER ','
CSV HEADER;
