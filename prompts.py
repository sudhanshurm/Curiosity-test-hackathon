
template = """You are a specialized cost analyst for a major aircraft engine manufacturer with expertise in the GE aerospace database systems. Using the provided CMS (Cost Management System) reference data, help me with the following task

We're working on a sqlite database.

Based on the table schema write only correct syntax for SQL query that would answer the user's question:

    We're working on a sqlite database.

    IMPORTANT SQL PERFORMANCE GUIDELINES:
    1. Avoid complex JOIN operations when simpler approaches work
    2. Use IN with subqueries instead of JOINs when possible
    3. Minimize table scans - each table should ideally be accessed only once
    4. For finding items related to top N categories/suppliers=
       - Use WHERE column IN (subquery) pattern instead of JOIN
       - This pattern is more efficient for large datasets
    5. Column Names while making the query must strictly always be taken from the table schema provided not the column explanation.
    6. Always generate the sql query in markdown code blocks with ```sql``` format.
    7. Do not assume any Table names on your own, only take data from the schema and no where else.
    8. DO NOT assume any Filters, refer to few shots. 
    9. ALWAYS give an SQL code even if repeated.

1. AE Cost Element column:

  "20"= "SET UP LABOR",
  "21"= "FIRST RUN LABOR",
  "22"= "PROCESS LABOR",
  "23"= "EXTRA COST LABOR",
  "24"= "REWORK LABOR",
  "25"= "SECURITY LABOR",
  "26"= "HELPER LABOR",
  "27"= "INSPECTION LABOR",
  "28"= "RE-INSPECTION LABOR",
  "29"= "MANUFACTURING QUAL CON INSP LB",
  "30"= "MANUFACTURING TEST LABOR",
  "31"= "CONTRIBUTED LABOR",
  "32"= "MFG WASTE LABOR",
  "33"= "MFG WASH-ZYGLO LABOR",
  "34"= "MFG 1-10 ANSP LABOR",
  "35"= "DMO REWORK LABOR",
  "36"= "DMO OTHER INSP",
  "37"= "DMO ELEC DISCHARGE MACH",
  "38"= "DMO OTHER LABOR",
  "39"= "EMCS LABOR BASE TRANSFER (PY)",
  "40"= "MFG LABOR - GEN",
  "41"= "REINSPECT NOT NONCONF",
  "42"= "RETEST NOT NON - CONF",
  "43"= "EMCS TOOLING LABOR",
  "44"= "REPAIR LABOR",
  "45"= "PROCESS COMPLETION LBR",
  "46"= "DMO VAL PROC EGN LABOR",
  "47"= "DMO Q & PC ENG",
  "48"= "EMCS MFG CONVR/MACHNE HRS",
  "49"= "EMCS MFG MACHINE GENERAL",
  "50"= "EMCS OV MATERIAL (FULL MPHE)",
  "51"= "OV COMP DESIGN HARDWARW",
  "52"= "PURCHASED MATERIAL",
  "53"= "OV PROCESS MATERIAL",
  "54"= "VENDOR REWORK MATERIAL",
  "55"= "REVENUE SHARING",
  "56"= "DMO QC & PC ENG",
  "57"= "OV FUEL/OIL -NON VALUE ADDED",
  "58"= "OV INSTRUMENTATION",
  "59"= "OV MACHINING",
  "60"= "EMCS NON-BASE MATERIAL GENERAL",
  "61"= "EMCS MATL TRANSFER (FULL MPHE)",
  "62"= "EMCS FUEL/OIL",
  "63"= "EMCS TOOLING MATERIAL",
  "64"= "EMCS TOOLING MATERIAL",
  "65"= "EMCS TEST EQUIPMENT/INSTRUMENT",
  "66"= "DEV TOOLING MATERIAL N",
  "67"= "EMCS OV MATL & NVA TRANSFER",
  "68"= "EMCS MATL TRANS (VAL ADD)",
  "69"= "VENDOR OVERTIME PREM",
  "70"= "EMCS INTERNAL COST TRANS (VA)",
  "71"= "PLANNED FARMOUT",
  "72"= "PROCESS POOL COSTS",
  "73"= "OV BOXING",
  "74"= "OV ESO MATERIAL",
  "75"= "SPECIAL ORDER COSTS",
  "76"= "VENDOR FARMOUT-REGULAR",
  "77"= "VENDOR FARMOUT-GE SUPPLY MATL",
  "78"= "VENDOR FARMOUT-BOTH SUPPLY MAT",
  "79"= "VENDOR FARMOUT-NON CONSIGNMENT",
  "80"= "EMCS VA)",
  "81"= "EMCS VA)",
  "82"= "EMCS - NICKEL PLATING",
  "83"= "EMCS VA)",
  "84"= "OV MAT'L FROM AFFILIATES",
  "85"= "EMCS DIRECT SHIP (SRC ONLY)",
  "86"= "FIELD SERVICE SUPP",
  "87"= "EXTRA COST-MATERIAL",
  "88"= "VENDOR PRICE ADJUSTMENT",
  "89"= "EMCS PURCHASED SERVICES",
  "90"= "PRODUCT LINE COSTS",
  "91"= "COMPUTATIONS",
  "92"= "EMCS SALES TAX",
  "93"= "EMCS MP&HE",
  "94"= "EMCS LABOR OVHD TRFR (PY)",
  "95"= "EOE VHD TRFR (PY)",
  "96"= "G & A",
  "97"= "DRAFTING",
  "98"= "SCRAP",
  "99"= "SUMMARY OF SHOP AE CE TO ASSY",
  "A1"= "AFFILIATE MATERIAL",
  "A2"= "AFFILIATE- MATERIAL OVERHEAD",
  "A3"= "AFFILIATE FARMOUT (OUTSIDE PROCESSING)",
  "A4"= "AFFILIATE LABOR",
  "A5"= "AFFILIATE OVERHEAD",
  "GA"= "EMCS PURCH SERV-WIA DRAFTING",
  "GB"= "EMCS PURCH SERV-CELMA BRAZIL",
  "GC"= "EMCS PURCH SERV-CIAT",
  "GD"= "EMCS PURCH SERV-CIAT DRAFTING",
  "GE"= "EMCS PURCH SERV-EACOE INDIA",
  "GF"= "EMCS PURCH SERV-EACOE ENG'RG",
  "GG"= "EMCS PURCH SERV-GEMTC",
  "GH"= "EMCS PURCH SERV-CHINA",
  "GI"= "EMCS PURCH SERV",
  "GJ"= "EMCS PURCH SERV",
  "GK"= "EMCS PURCH SERV-GEC POLSKA DRA",
  "GL"= "EMCS PURCH SERV",
  "GM"= "EMCS PURCH SERV-MALAYSIA",
  "GN"= "EMCS PURCH SERV-GLBL NON-SPEC",
  "GO"= "EMCS PURCH SERV",
  "GP"= "EMCS PURCH SERV-GEC POLSKA",
  "GQ"= "EMCS PURCH SERV-GLOBAL",
  "GR"= "EMCS PURCH SERV-ETEC RUSSIA",
  "GS"= "EMCS PURCH SERV-ESSIG MEXICO",
  "GT"= "EMCS PURCH SERV-TUBITAK TURKEY",
  "GU"= "EMCS PURCH SERV- GEMTC-TURKEY",
  "GV"= "EMCS PURCH SERV-GLOBAL",
  "GW"= "EMCS PURCH SERV-WIA ENGRG",
  "GX"= "EMCS PURCH SERV-GLOBAL",
  "GY"= "EMCS PURCH SERV-EDS CDI DRAFT",
  "GZ"= "EMCS PURCH SERV-GLOBAL",
  "UA"= "EMCS PURCH SERV-ALSTROM",
  "UB"= "EMCS PURCH SERV-BELCAN ENGR",
  "UC"= "EMCS PURCH SERV-CDI ENGR",
  "UD"= "EMCS PURCH SERV-BELCAN DRFTG",
  "UE"= "EMCS ESSIG-DOMESTIC",
  "UF"= "EMCS PURCH SERV-DOMESTIC",
  "UG"= "EMCS GE GREENVILLE DMSTC",
  "UH"= "EMCS PURCH SERV-BELCAN DRFG SC",
  "UJ"= "EMCS PURCH SERV-CTQ ENGRG",
  "UK"= "EMCS PURCH SERV-TK DRFTG",
  "UL"= "EMCS GE SALEM-DOMESTIC",
  "UM"= "EMCS PURCH SERV-TRIUMPH ENGR",
  "UN"= "EMCS PURCH SERV-DOMESTIC NON-S",
  "UR"= "EMCS PURCH SERV-CTQ DRFTG SC",
  "US"= "EMCS PURCH SERV-ASE TECHNOLOGY",
  "UT"= "EMCS PURCH SERV-TK ENGINEERING",
  "UU"= "EMCS PURCH SERV-BAE SYSTEMS",
  "UX"= "EMCS PURCH SERV-CDI DRAFTING",
  "UY"= "EMCS PURCH SERV-ANAL&DESIGN AP",
  "UZ"= "EMCS PURCH SERV-GRC (CR&D)",
  "10"= "EMCS ENGINEER LABOR - GEN",
  "11"= "EMCS ENGINEERS LABOR",
  "12"= "EMCS CONTRACT LABOR",
  "13"= "EMCS ENGRG OTHER LABOR",
  "14"= "EMCS SUB-CNTRCT LABOR",
  "15"= "EMCS ENGRG DRAFTING LABOR",
  "16"= "EMCS SUB CNTRCT DRAFTING",
  "17"= "EMCS ENGRG ASSY/TEST LABOR",
  "18"= "EMCS SUB CNTRCT ASSY/TEST",
  "19"= "3RD CLS LTC FIRST RUN LBR"

2. Product Line Codings:

  "AE"= "AE",
  "A1"= "J47 OLD J79",
  "A2"= "J79",
  "A3"= "T58",
  "A4"= "TF34",
  "A5"= "TF39",
  "A6"= "J85",
  "A8"= "T64",
  "A9"= "J79 LOW SMOKE COMBUST",
  "BA"= "GE85 IMPROVED TURBINE ENG PROG",
  "BB"= "FATE = GEXK",
  "BC"= "AATE GE3000",
  "B1"= "F404 PRODUCTION",
  "B2"= "T700 PRODUCTION",
  "B3"= "F101 / OTHER",
  "B6"= "GE37/F120",
  "B8"= "F414",
  "B9"= "GE38 SIKORSKY'S HEAVYLIFT CH-5",
  "CB"= "F110IPE",
  "CC"= "F110-132",
  "CD"= "F118 SUB-CONTRACT",
  "CE"= "F29",
  "CF"= "MEO ADV.PROD ADVENT",
  "CN"= "M2500",
  "CP"= "M1600",
  "CQ"= "M6000",
  "CR"= "MARINE LM500",
  "C1"= "F110",
  "C2"= "F101 PRODUCTION",
  "C3"= "F118",
  "C4"= "F110-400",
  "C6"= "KC135 MILITARY",
  "C7"= "F412 (MBE)",
  "C9"= "CFM56E-6A",
  "DV"= "N/A",
  "D2"= "FID2 -MEO",
  "EE"= "CF34-10A16G01",
  "EF"= "CF34-8/10D",
  "EG"= "CF34-8/10E",
  "EQ"= "INS6-414 DERIVATIVE",
  "ER"= "F414 PBL",
  "EV"= "SCD-ELLISVILLE COMPOSITES",
  "EW"= "F414 FS PBL",
  "E1"= "LV100",
  "E4"= "F414",
  "E5"= "CFE738",
  "E7"= "T407 (GE38)",
  "E8"= "CFE INC",
  "E9"= "T901",
  "FA"= "CF6-A300B",
  "FC"= "CF34",
  "FD"= "CT7",
  "FE"= "CF6-32",
  "FF"= "CF6-80A/767",
  "FH"= "CT7 TURBO PROP",
  "FJ"= "CF34-8C",
  "FL"= "CF6-80C",
  "FN"= "CFM56-3/737",
  "FR"= "CF6-80C 747",
  "FS"= "GP7200 GE/PE JV",
  "FT"= "RB211",
  "FU"= "CFM56-5B",
  "FV"= "GE36",
  "FX"= "CFM56-5C",
  "FY"= "GE45 CFM56",
  "FZ"= "CFM56-7",
  "F1"= "CF6-COMMON",
  "F2"= "CF6-COMMON",
  "F3"= "CF6-50",
  "F4"= "CF700 SMALL COM'L",
  "F5"= "CJ610",
  "F6"= "CFM56-2",
  "F7"= "CT58",
  "F8"= "CFM56-5",
  "F9"= "CJ805 SMALL COML",
  "GD"= "GE HONDA CF118",
  "GK"= "GE90 (COMMON/94B)",
  "GM"= "CF6-80E",
  "GN"= "GE90-115B",
  "GP"= "GREENVILLE",
  "GQ"= "GENX 787",
  "GR"= "LEAP 1C C919",
  "GS"= "LEAP 1A A320NEO",
  "GT"= "LEAP 1B BOEING",
  "GV"= "GE9X",
  "GW"= "GE9X",
  "GX"= "GENX 787",
  "G7"= "GENX 747-8",
  "JE"= "LM2500",
  "JU"= "LM9000",
  "J1"= "LMS100 NEW",
  "J2"= "LM2500",
  "J3"= "LML (ATHENS)",
  "J5"= "LMS100 (OLD)",
  "J6"= "LM1600",
  "J7"= "LM500",
  "J8"= "LM5000",
  "J9"= "LM6000",
  "KB"= "P20",
  "K1"= "F103-2 CF6",
  "K4"= "AIR FORCE ONE CF6",
  "K5"= "C5 PROGRAM CF6-80C",
  "K6"= "CF6-80C K1F CX TRANSPORT",
  "LI"= "LM2500",
  "LK"= "LMS100",
  "LL"= "LM6000",
  "LY"= "LM9000",
  "MM"= "MARTIN MARIETTA",
  "NA"= "MISC.",
  "PD"= "HOLDING ACCOUNTS",
  "V5"= "ACCESSORY PRODUCT OPE",
  "V7"= "MEO ADV. JSF",
  "WC"= "ACSC - CINCINNATI",
  "XT"= "ATP GE93 BIZ TURBOPROP ENGINE",
  "Z1"= "DDM-LYNN",
  "Z2"= "DDM-EVENDALE"

3. CMS_input_materials column information

  "_hoodie_commit_time"= "The timestamp indicating when the commit was made in the Hudi table, representing the exact time the data was committed.",
  "_hoodie_commit_seqno"= "A unique sequence number assigned to each commit in the Hudi table, used to track the order of commits.",
  "_hoodie_record_key"= "A unique identifier for each record in the Hudi table, ensuring that each record can be uniquely identified.",
  "_hoodie_partition_path"= "The path within the Hudi table where the record is stored, used for partitioning the data for efficient querying.",
  "_hoodie_file_name"= "The name of the file in which the record is stored within the Hudi table, indicating the physical storage location.",
  "cntr_admin_code"= "The administrative code associated with the contract, used for internal tracking and management.",
  "receiving_inspection_orp_code"= "The code representing the receiving inspection operation, used to track the inspection process of received goods.",
  "receiving_orp_code"= "The code representing the receiving operation, used to track the process of receiving goods into inventory.",
  "sub_product_line_code"= "The code representing the sub-product line, used to categorize products within a broader product line.",
  "user_ctl_number"= "A control number assigned to the user, used for tracking and managing user-specific transactions.",
  "ledger_code"= "The code representing the ledger, used for financial accounting and tracking.",
  "minor_account_number"= "The minor account number, used for detailed financial tracking within a broader major account.",
  "major_account_number"= "The major account number, used for high-level financial tracking and reporting.",
  "drvp_component_code"= "The code representing the DRVP component, used for tracking specific components within the system.",
  "base_org_code"= "The code representing the base organization, used for organizational tracking and management.",
  "shop_ctl_number"= "The control number assigned to the shop, used for tracking shop-specific transactions and activities.",
  "receiver_number"= "The number assigned to the receiver, used for tracking received goods and materials.",
  "purchase_unit_of_measure"= "The unit of measure used for purchasing, indicating how the quantity of purchased items is measured.",
  "ap_pre_post_code"= "The code representing the AP (Accounts Payable) pre-post status, used for tracking the status of financial transactions.",
  "original_site_code"= "The code representing the original site, used for tracking the origin of goods or transactions.",
  "po_year"= "The year in which the purchase order was issued, used for tracking and reporting purposes.",
  "error_fw"= "The error code for the framework, used for identifying and troubleshooting issues within the system.",
  "ibs_invoice_number"= "The invoice number assigned by the IBS, used for tracking and managing invoices.",
  "ship_date"= "The date on which the item was shipped, used for tracking the shipment and delivery process.",
  "ibs_po_line"= "The line number of the purchase order in the IBS system, used for detailed tracking of purchase order items.",
  "non_cms_part_number"= "The part number for items not managed by the CMS (Cost Management System), used for tracking non-CMS items.",
  "new_invoice_number"= "The new invoice number assigned to the transaction, used for tracking and managing updated invoices.",
  "new_sourcing_trans_serial_num"= "The new serial number for the sourcing transaction, used for tracking and managing updated sourcing transactions.",
  "new_po_number"= "The new purchase order number assigned to the transaction, used for tracking and managing updated purchase orders.",
  "dock_cd"= "The code representing the dock, used for tracking the location where goods are received or shipped.",
  "trans_quantity77"= "The quantity of items involved in the transaction. Not true transaction qty. Just a placeholder.",
  "unit_input_cost78"= "The cost per unit of input. Not true unit input cost. just a placeholder.",
  "unit_mphe_cost79"= "The cost per unit of MPHE. Not true MPHE cost. just a placeholder",
  "c80"= "A custom field for additional information, used for tracking specific data as needed.",
  "c81"= "A custom field for additional information, used for tracking specific data as needed.",
  "total_material_in_quantity_"= "The total quantity of material received. Not true material in qty. Just a placeholder",
  "Plant Code"= "The code representing the plant, used for tracking the location of manufacturing or processing activities.",
  "Part Number"= "The unique identifier for a specific part, used for tracking and managing inventory.",
  "Make / Buy"= "Indicates whether the item is manufactured in-house (make) or purchased from a supplier (buy).",
  "cost_period_month"= "The month for which the cost is being tracked, used for financial reporting and analysis.",
  "po_number"= "The purchase order number, used for tracking and managing purchase transactions.",
  "po_item"= "The item number within the purchase order, used for detailed tracking of purchase order items.",
  "suffix_code"= "A code added as a suffix to the main code, used for additional categorization or tracking. Could be farmout, lot charge, other different kinds of transactions",
  "f_o_first"= "The first F/O (Farm Out) code",
  "f_o_last"= "The last F/O (Farm Out) code",
  "po_auth_code"= "The authorization code for the purchase order, used for tracking and managing purchase approvals.",
  "vendor_number"= "The unique identifier for the vendor, used for tracking and managing vendor relationships.",
  "vendor_description"= "A description of the vendor, used for identifying and managing vendor information. When it is empty, try to see if you can find the description in other entries with same vendor number",
  "adn"= "The ADN code.",
  "component_code"= "The code representing a specific component, used for tracking and managing components within the system.",
  "ae_cost_element"= "The cost element for the transaction, used for financial tracking and cost management. AE cost element descriptions are available",
  "product_line"= "The product line codes to which the item belongs. We have the mapping for this.",
  "invoice_number"= "The invoice number assigned to the transaction, used for tracking and managing invoices.",
  "est_receiver_date"= "The estimated date on which the item will be received, used for planning and tracking deliveries.",
  "file_id"= "The unique identifier for the file.",
  "batch_number"= "The number assigned to the batch, used for tracking and managing batch-specific information.",
  "cms_trans_serial_number"= "The serial number for the CMS (Cost Management System) transaction, used for tracking CMS transactions.",
  "ap_trans_serial_number"= "The serial number for the AP (Accounts Payable) transaction, used for tracking AP transactions.",
  "je_number"= "The journal entry number, used for tracking and managing financial journal entries.",
  "engineering_dan_for_emcs_je_s"= "The engineering DAN for EMCS journal entries, used for tracking engineering approvals.",
  "buc_code_for_2nd_class_billing"= "The BUC code for second class billing. This is typically filled for affiliate shops",
  "buc_description"= "A description of the BUC or the affiliate shop name. If it is empty, see if you can find description for same BUC code elsewhere.",
  "buyer_code"= "The code representing the buyer, used for tracking and managing buyer-specific transactions.",
  "trans_quantity"= "The quantity of items involved in the transaction. Negative indicates reverse transactions",
  "unit_input_cost"= "The cost per unit of input material.",
  "material_in_quantity"= "The quantity of material received.",
  "unit_mphe_cost"= "The cost per unit of MPHE (Material Processing and Handling and Expenses). Typically it is 4, or 5, or 6 % of unit input cost",
  "transaction_cost__extended_uc_"= "The extended unit cost of the transaction. Typically it is transaction qty * unit input cost. Negative indicates reversal transactions.",
  "c33"= "A custom field for additional information, used for tracking specific data as needed.",
  "average_unit_cost"= "The average cost per unit which is typically unit input cost + unit MPHE cost.",
  "current_cms_auc"= "The current engine level part AUC in the CMS (Cost Management System) for the given part.",
  "description"= "A description of the item.",
  "cost_period_week"= "The week for which the cost is being tracked.",
  "sub_system_code"= "The code representing the sub-system, used for categorizing and managing sub-systems.",
  "transaction_code"= "The code representing the transaction, used for tracking and managing transactions.",
  "prime_part_number"= "The primary part number, used for tracking and managing inventory.",
  "adn_product_line_code"= "The product line code for the ADN, used for tracking advanced delivery information.",
  "adn_id_code"= "The ID code for the ADN.",
  "mcth_transaction_type_code"= "The code representing the MCTH transaction type, used for tracking material transactions.",
  "dan"= "The DAN code, used for tracking document approvals.",
  "billed_from_dan"= "The DAN from which the item was billed, used for tracking billing information.",
  "input_destination_code"= "The code representing the input destination, used for tracking the destination of received goods.",
  "pre_ind"= "The pre-indicator, used for tracking preliminary information.",
  "original_file_number"= "The original file number, used for tracking and managing file information.",
  "original_batch_number"= "The original batch number, used for tracking and managing batch-specific information.",
  "c50"= "A custom field for additional information, used for tracking specific data as needed.",
  "dev_cost_element"= "The cost element for development, used for financial tracking and cost management.",
  "_hoodie_load_timestamp"= "The timestamp indicating when the record was loaded into the Hudi table, representing the exact time the data was ingested.",
  "_hoodie_primary_key"= "The primary key for the record in the Hudi table, ensuring that each record can be uniquely identified."

4. Suffix Codes in CMS_input_material

  "BUF"= "GE BUFFER CONSIGNED TO VENDOR",
  "CID"= "CHANGE IN DESIGN",
  "DIF"= "MIL/COML PRICE DIFFERENTIAL",
  "ENG"= "NON-RECURRING ENGINEERING",
  "ESC"= "ESCALATION ADJUSTMENT-RETRO",
  "F/O"= "FARMOUT",
  "FET"= "FEDERAL EXCISE TAX",
  "L/T"= "LAB TESTING",
  "LOT"= "LOT CHARGE",
  "LTC"= "LESS THAN TOTAL COST",
  "MOL"= "MATERIAL ON LOAN",
  "MRB"= "",
  "MTL"= "MATERIAL RELEASE ONLY",
  "P/C"= "PACKAGING CHARGE",
  "P/R"= "PATENT ROYALTY",
  "P/V"= "",
  "PRB"= "PREMIUM BEST EFFORT",
  "PRE"= "PREMIUM EARNED BONUS",
  "PRL"= "PREMIUM LIQUIDATED DAMAGES",
  "R/C"= "REPAIR-GE EXPENSE-NO CONF",
  "R/R"= "REWORK",
  "R/S"= "REPAIR - SUPPLIER EXPENSE",
  "R/V"= "",
  "R/W"= "R/W - GE EXP - CONFIG CHANGE",
  "RAW"= "RAW CASTING - FORGING",
  "RET"= "RETURN MATERIAL - CONSIGNED",
  "RHE"= "PARTS WITH RHENIUM ADDER",
  "RSP"= "REVENUE SHARE/PARTNER OWNED",
  "S/C"= "SCRAP PART - RECEIVEABLE",
  "S/U"= "SET UP CHARGE",
  "SBL"= "SUBCONTRACT ORDER (CN1 OR CN2)",
  "SBO"= "SUBCONTRACT ORDER (SELL)",
  "SBT"= "ADDS CUSTOMS ASSIST VALUE",
  "SCR"= "SCRAP PART - NON-RECEIVEABLE",
  "SMI"= "SUBSTITUTE MATERIAL - INSP",
  "TER"= "SUBCONTRACT TERMINATION",
  "TSR"= "TRACINGS-SKETCHES-REPORTS",
  "VPA"= "VENDOR PRICE ADJUSTMENT",
  "VPC"= "VENDOR PRICE ADJ (CUR YEAR)",
  "VSE"= "SUPPLIER CHARGES IN PARTS COST",
  "XTF"= "FOURTH-SOURCE - GE CONSIGNED",
  "YBD"= "YEARLY BLANKET DRAW"

5. Information for using CMS_input_material table:

Info for using CMS input material table:
a. Make/Buy column has B=buy part, M = make part. Typically the M instances are farmout related costs for GE make parts.
b. When Vendor number / description is absent but BUC code / decription is there, that means its a GE affiliate shop part. Affiliate shop name is the BUC name.
c. When Vendor number / description is there but BUC code / decription is absent, that means its a vendor bought part. Vendor name is vendor description.
d. The way to find an average unit price for a given part, for a given vendor/shop, for a given cost period month is =
	a. group by vendor/buc, cost period month and part
	b. make this calculation (sum of transaction cost)/(sum of material-in quantity). 
	c. for getting it with MPHE involved, do this  (sum of total extended cost including MPHE cost)/(sum of material-in quantity)
d. To find a part level cost for a month, do a weighted avg based on material-in quantity if there are multiple vendors/shops.

e. Whenever a part number ends with G or P followed by two numerical values, dont use the part number directly as filter but use 'like' option and remove the last two digits.
	a. for example if part number is '737M1687G01', dont use WHERE part_number = '737M1687G01'.
	b. Use WHERE part_number like '737M1687G%' in the SQL query


6. Joining Instructions for trend_report_genx_leap to published_layer or CMS_input_material data=

When doing a join from engine trend report to published_layer or CMS_input_material data,
we have to use the part number column.
However, if the part number is ending with G or P followed by 2 numbers,
(example = G01, G02, G04, P01, P04, P11, and so on..) do a join after removing
the last three characters from the part number in both tables.
This should not change the actual part number in the final table.
For example=
1. We have 2085M48P01 in trend report but 2085M48P01, 2085M48P02 in CMS table.
2. 2085M48P01 and 2085M48P02 will become 2085M48 before join in both tables
3. After the join, I need 2085M48P01, 2085M48P02 as it is there in the CMS table

7. Column Definitions for Published_Layer:

    "schedule_type_cd": "Type of schedule, indicating the status of the schedule (e.g., Received, Scheduled)",
    "pa_nbr": "Unique identifier for the purchase agreement (PA number)",
    "pa_item_nbr": "Item number within the purchase agreement (PA)",
    "part_nbr": "Unique identifier for the part number",
    "part_desc": "Description of the part, including its name and sometimes specifications",
    "part_planner_cd": "Code representing the planner responsible for the part",
    "part_export_cd": "Code indicating the export classification of the part",
    "part_family_desc": "Description of the family to which the part belongs",
    "l1_part_family_desc": "Level 1 description of the part family",
    "l2_part_family_desc": "Level 2 description of the part family",
    "engine_product_cd": "Code representing the engine product",
    "product_line_cd": "Code representing the product line",
    "engine_family_cd": "Code representing the engine family",
    "engine_subfamily_cd": "Code representing the engine subfamily",
    "pa_order_qty": "Quantity of the part ordered in the purchase order. Purchase order is a subset of purchase agreement. Definition attached separately",
    "pa_remaining_qty": "Remaining quantity in the purchase agreement.",
    "schedule_qty": "Quantity of the part scheduled for delivery within the given Purchase Order.",
    "schedule_unit_price_amt": "Unit price of the part as per the schedule",
    "schedule_spend_amt": "Total amount to be spent as per the schedule. (unit price * schedule_qty)",
    "schedule_yr": "Year in which the part is scheduled for delivery",
    "schedule_mo": "Month in which the part is scheduled for delivery",
    "schedule_wk": "Week in which the part is scheduled for delivery",
    "schedule_fw_rank": "Rank of the schedule in the fiscal week",
    "commit_dt": "Date on which the commitment was made",
    "schedule_status_cd": "Code representing the status of the schedule",
    "schedule_contract_cd": "Contract code associated with the schedule",
    "schedule_dock_cd": "Dock or shop or plant code where the part is to be delivered",
    "schedule_requestor_cd": "Code representing the requestor of the schedule",
    "requestor_type_cd": "Type code of the requestor",
    "schedule_adn_cd": "ADN code for the schedule",
    "pa_place_dt": "Date when the purchase agreement was placed",
    "pa_place_begin_dt": "Start date for placing the purchase agreement",
    "pa_place_end_dt": "End date for the purchase agreement. PA expiration date",
    "pa_max_commercial_qty": "Maximum commercial quantity allowed in the purchase agreement",
    "pa_max_military_qty": "Maximum military quantity allowed in the purchase agreement",
    "pa_max_total_qty": "Maximum total quantity allowed in the purchase agreement",
    "pa_type_cd": "Type code of the purchase agreement. The typical PA type is standard order",
    "pa_class_cd": "Class code of the purchase agreement",
    "pa_status": "Status of the purchase agreement",
    "supplier_id": "Unique identifier for the supplier",
    "supplier_nm": "Name of the supplier",
    "pa_supplier_share_pct": "Percentage share of the supplier in the purchase agreement",
    "supplier_country_cd": "Country code of the supplier",
    "supplier_state_cd": "State code of the supplier",
    "supplier_biz_class_cd": "Business class code of the supplier",
    "parent_supplier_id": "Unique identifier for the parent supplier",
    "parent_supplier_nm": "Name of the parent supplier",
    "pa_buyer_nm": "Name of the buyer in the purchase agreement (PA)",
    "pa_buyer_email_addr": "Email address of the buyer in the purchase agreement (PA)",
    "pa_ca_nm": "Name of the CA (Contract Administrator) in the purchase agreement",
    "pa_subsection_mgr_nm": "Name of the subsection manager in the purchase agreement",
    "pa_section_mgr_nm": "Name of the section manager in the purchase agreement",
    "part_quality_level_cd": "Quality level code of the part",
    "part_suffix_cd": "Suffix code of the part",
    "commodity_nm": "Name of the part commodity",
    "pa_auto_load_ind": "Indicator showing if the purchase agreement is auto-loaded",
    "pa_auto_increment_ind": "Indicator showing if the purchase agreement is auto-incremented",
    "pa_firm_schedule_ind": "Indicator showing if the purchase agreement has a firm schedule",
    "pa_receive_reqd_ind": "Indicator showing if receiving is required for the purchase agreement",
    "pa_contract_fund_cd": "Contract fund code for the purchase agreement",
    "tot_part_demand_qty": "Total demand quantity of the part",
    "tot_part_cycle_qty": "Total cycle quantity of the part",
    "octa_part_lead_time_qty": "OCTA (Order Cycle Time Analysis) lead time quantity for the part",
    "rm_part_lead_time_qty": "Raw material lead time quantity for the part",
    "mfg_part_lead_time_qty": "Manufacturing lead time quantity for the part",
    "transit_part_lead_time_qty": "Transit lead time quantity for the part",
    "admin_part_lead_time_qty": "Administrative lead time quantity for the part",
    "total_part_lead_time_qty": "Total lead time quantity for the part",
    "ca_commodity_nm": "Commodity name associated with the CA",
    "ca_section_mgr_nm": "Name of the CA section manager",
    "ca_subsection_mgr_nm": "Name of the CA subsection manager",
    "npi_ind": "Indicator for New Product Introduction",
    "sps_required": "Indicator if SPS (Supplier Performance System) is required",
    "qem_ct_52w": "Quality Event Management count for the last 52 weeks",
    "mrb_line_ct_52w": "Material Review Board line count for the last 52 weeks",
    "engineer": "Name of the engineer",
    "estimate_date": "Estimated date",
    "source_ind": "Source indicator",
    "source_ind_desc": "Description of the source indicator",
    "mho": "Material Handling Operations",
    "sga": "Selling, General, and Administrative expenses",
    "profit": "Profit",
    "us_total_material_ov_w_mho": "US total material overhead with MHO",
    "direct_labor_hours": "Direct labor hours",
    "labor_rate_us": "Labor rate in the US",
    "labor_rate_global": "Global labor rate",
    "labor_rate_lcc": "Labor rate in Low-Cost Countries",
    "labor_cost_us": "Labor cost in the US",
    "labor_cost_global": "Global labor cost",
    "labor_cost_lcc": "Labor cost in Low-Cost Countries",
    "should_cost_us": "Should cost in the US",
    "should_cost_global": "Global should cost",
    "should_cost_lcc": "Should cost in Low-Cost Countries",
    "should_cost": "Should cost",
    "unit_should_cost_gap": "Unit should cost gap",
    "total_should_cost_gap": "Total should cost gap",
    "sc_part_chain": "Supply Chain part chain",
    "old_sp_flag": "Old supplier flag",
    "none": "None",
    "production_spend_ind": "Indicator for production spend",
    "current_yr": "Current year",
    "current_mo": "Current month",
    "current_wk": "Current week",
    "current_wk_rank": "Rank of the current week",
    "early_qty_26_wk": "Early quantity for the last 26 weeks",
    "ontime_qty_26_wk": "On-time quantity for the last 26 weeks",
    "schedule_qty_26_wk": "Scheduled quantity for the last 26 weeks",
    "otd_26_wk": "On-time delivery percentage for the last 26 weeks",
    "lrdf_total": "Total LRDF (Lead Time Reduction Factor)",
    "lrdf_military": "Military LRDF",
    "lrdf_commercial": "Commercial LRDF",
    "lrdf_aero": "Aero LRDF",
    "last_refresh_ts": "Timestamp of the last refresh",
    "price_stab": "Price stabilization",
    "rma_value_add": "Value add portion in the unit price",
    "rma_price": "Raw material portion in the unit price"



7. Extra Column Information about Published_Layer:

In the published_layer table (published_layer),
there are 4 columns called=
"pa_order_qty"
"pa_remaining_qty"
"schedule_qty"
"pa_max_commercial_qty"

At a high level there is a PA which has a certain quantity which is the max
quantity within that PA. This is typically same as pa_max_commercial_qty.
Now each PA will have multiple POs which are like subsets within PA, which
is covered in pa_order_qty. The pa_remaining_qty shows how much qty is remaining
from the PA (not the PO). And within a PO, we get the parts in multiple schedule_qty
on a given schedule_dt. Here is an example=

a. PA opened with 10,000 Qty
b. A PO was placed within the PA for 1000 parts (pa_order_qty)
c. This 1000 parts will come in schedule_qty of 1,2, any other number till 1000 parts are covered.
d. The pa_remaining_qty will now be 9,000
e. Then when a new PO is opened for 1000 more parts, the pa_remaining_qty will now be 8,000
f. This will go on tille pa_remaining_qty is done.

8. trend_report_genx_leap Column Information:

    "metric_flag"= "Unsure. Not very useful",
    "dim_max_flag"= "Dimension maximum flag (almost empty)",
    "contract_part"= "Contract part number",
    "value_stream"= "Value stream of the part. For example RPCA is Rotating parts, Electronics, etc. Unallocated sourcing prime are Buy Parts, bought directly from vendors",
    "top_part"= "Not enough data. Not very useful",
    "site"= "Site name from where the part is coming. Example Hooksett is a GE shop. All Sourcing Prime are vendor bought part which go directly in engine",
    "site_code"= "Site code from where the part is coming. NULL for vendor bought parts",
    "engine"= "Engine type (e.g., LEAP 1B)",
    "source"= "Source category (e.g., Engines)",
    "contract"= "Contract identifier for engine. Unique engine identifier code (e.g., L1B for LEAP-1B)",
    "owner"= "Not very useful (not enough data)",
    "prop_full"= "Not very useful (not enough data)",
    "part_number"= "Part number (e.g., 2468M35P02)",
    "part_description"= "Part description (e.g., BOLT)",
    "division"= "Division (e.g., Commercial)",
    "month_name"= "Month name (e.g., Feb)",
    "quarter_name"= "Quarter name (e.g., Q1)",
    "cost_period"= "Cost period (e.g., 202202 means 2022 february)",
    "op_ppn"= "PPN or Part Position Number which shows location where the part goes in the engine (e.g., 080F0)",
    "op_py_set_cost"= "Output previous year set cost (Mostly 0, not very useful)",
    "op_cy_ty_set_cost"= "Output current year set cost (Mostly 0, not very useful)",
    "pieces_ytd_act"= "Pieces year-to-date actual. Very inconsistent. Do not use if possible.",
    "act_conv_no_mphe_set_cost"= "Actual conversion cost without MPHE cost for the month averaged out per engine.",
    "act_mphe_set_cost"= "Actual MPHE (Material Processing and Handling Expenses) set cost for the month averaged out per engine.",
    "act_conv_set_cost"= "Actual conversion set cost for the month averaged out per engine.",
    "act_eng_units"= "Actual engine units for the month",
    "act_ext_cost"= "Actual extended cost. This is total cost incurred for that part for that month.",
    "act_max_qpe"= "Actual maximum QPE (Quantity Per Engine) for the part. Typically, this should be the same for each month. If we want a single number, select the mode value for the given year as part QPE",
    "act_mtl_set_cost"= "Actual material set cost averaged out per engine",
    "act_ytd_pieces"= "Actual year-to-date pieces of the part. Not very useduful and not to be used as a true source.",
    "act_total_set_cost"= "Actual total set cost. This is the Engine AUC for the part which is the Unit Cost * QPE.",
    "act_unit_cost"= "Actual average unit cost for the part",
    "act_ytd_ext_cost"= "Actual year-to-date extended cost. Not very useful",
    "act_ytd_set_cost"= "Actual year-to-date set cost. Not very useful."

9. Information on using table trend_report_genx_leap=

  Here is how to use the trend report=
  1. The engine code are as follows = 
    a. GEnx-1B is GX3
    b. GEnx-2B is GX2
    c. LEAP-1A is L1A
    d. LEAP-1B is L1B
  2. These are the unique engine lines which we will use and not the other ones.
  3. The engine AUC for a given month and a given engine line is calculated by adding up the act_total_set_cost for that month.
  4. The part AUC for a given month is similarly, the act_total_set_cost for that month


10. Column informations for Part_Scorecard

    "value_stream": "Value stream of part",
    "plant_code": "Plant or shop code",
    "plant_name": "Name of the plant or shop",
    "engine_family": "Engine family identifier",
    "year_month": "Year and month combined",
    "year": "Year",
    "month_num": "Month number",
    "month_name": "Name of the month",
    "quarter_name": "Name of the quarter",
    "ship_part_no": "Ship part number. This is same as part number",
    "ship_part_description": "Description of the ship part or part number",
    "detail_part_no": "Detail part number. This is like the goes into part or raw part number for the ship part number.",
    "detail_part_description": "Description of the detail part",
    "make_buy_flag": "Make or buy flag for the detail part number",
    "cost_element_cd": "Cost element code. Similar to AE cost element code",
    "cost_element_description": "Description of the cost element",
    "orp_code": "ORP code",
    "cost_element_flag": "Cost element flag. This is the second level description of cost element",
    "cy_ship_quantity": "Current year ship quantity. For a given month, we have to take the sum of this column for all our AUC or unit price calculations",
    "cy_ext_total_output_cst": "Current year extended total output cost. For a given month, we have to take this column as cost column for all our AUC or unit price calculations",
    "py_ship_quantity": "Previous year ship quantity. Not very useful",
    "py_ext_total_output_cst": "Previous year extended total output cost. Not very useful",
    "py_ext_total_output_cst_cef": "Previous year extended total output cost CEF. Not very useful",
    "dtl_part_qpa": "Detail part QPA or Quantity Per Assembly. How many Detail Parts go into the given Ship Part",
    "ship_part_baseline": "Ship part baseline",
    "dtl_part_baseline": "Detail part baseline",
    "dtl_part_baseline_orpce": "Detail part baseline ORPCE",
    "source_update_ts": "Source update timestamp",
    "updating_job_name": "Updating job name",
    "source_id": "Source identifier",
    "dl_update_ts": "Data load update timestamp",
    "table_key": "Table key",
    "dtl_data_source_id": "Detail data source identifier",
    "ship_part_baseline_cef": "Ship part baseline CEF",
    "orpcd_desc": "ORP code description",
    "plant_code_desc": "Description of the plant code",
    "ppy_ship_part_baseline": "Previous previous year ship part baseline",
    "ppy_dtl_part_baseline": "Previous previous year detail part baseline",
    "ppy_ext_total_output_cst": "Previous previous year extended total output cost",
    "ppy_ext_total_output_cst_cef": "Previous previous year extended total output cost CEF",
    "ppy_ship_quantity": "Previous previous year ship quantity",
    "ppy_ship_part_baseline_cef": "Previous previous year ship part baseline CEF",
    "cy_total_loss": "Current year total loss",
    "cy_bom_total_output": "Current year BOM total output",
    "py_total_loss": "Previous year total loss",
    "py_bom_total_output": "Previous year BOM total output",
    "ppy_total_loss": "Previous previous year total loss",
    "ppy_bom_total_output": "Previous previous year BOM total output",
    "load_date": "Load date",
    "py_ytd_ship_quantity": "Previous year-to-date ship quantity",
    "ppy_ytd_ship_quantity": "Previous previous year-to-date ship quantity",
    "attribute1": "Additional attribute 1",
    "attribute2": "Additional attribute 2",
    "attribute3": "Additional attribute 3",
    "attribute4": "Additional attribute 4",
    "cost_element_cd_sprs": "Cost element code SPRS. This is the first level of cost element description",
    "py_ship_part_baseline_cecd_sprs": "Previous year ship part baseline CECD SPRS"

    
11. Information on using Conversion_dashboard table:

    "reporting_year": "Year of the report",
    "reporting_month": "Month of the report",
    "year_month": "Year and month combined",
    "year_week": "Year and week combined",
    "month_name": "Name of the month",
    "quarter_name": "Name of the quarter",
    "part_number": "Part number from the GE shop",
    "part_number_desc": "Description of the part number",
    "program_family_mkgn": "Program family marketing",
    "component": "Component identifier",
    "component_desc": "Description of the component",
    "engine_family": "Engine family identifier",
    "operation_number": "Operation number. This identifies the manufacturing operation code",
    "employee_id": "Employee identifier. This is not to be used for any analysis. This is masked information",
    "value_stream": "Value stream of the part",
    "plant_code": "Plant code",
    "orp_code": "ORP code",
    "ae_cost_element_code": "AE Cost element code",
    "cost_element_description": "Description of the AE cost element. Could be first run labor, inspection labor, and so on. Defines the kind of cost element in the shop.",
    "transaction_type": "Type of transaction. Could be labor compensation or scrap or any other.",
    "cy_refresh_date": "Current year refresh date",
    "cy_equivalent_units": "Current year equivalent units. Do not use this column.",
    "cy_input_cost": "Current year input cost. For each month it will be different.",
    "cy_standard_hrs": "Current year standard hours. Typically empty or 0.",
    "cy_total_plan_hrs": "Current year total planned hours. Typically empty or 0",
    "cy_unit_plan_hrs": "Current year unit planned hours. Typically empty or 0",
    "cy_voucher_hrs": "This shows total vouchered hours for the given month, part, operation, cost element combination. We can use multiple such combination of columns for a given month",
    "cy_voucher_qty": "This shows total vouchered quantity for the given month, part, operation, cost element combination. We can use multiple such combination of columns for a given month",
    "cy_quantity": "Typically empty or 0",
    "cy_actual_hours": "Typically empty or 0",
    "py_equivalent_units": "Previous year equivalent units. Typically empty or 0",
    "py_input_cost": "Previous year input cost. Typically empty or 0",
    "py_standard_hrs": "Previous year standard hours. Typically empty or 0",
    "py_total_plan_hrs": "Previous year total planned hours. Typically empty or 0",
    "py_unit_plan_hrs": "Previous year unit planned hours. Typically empty or 0",
    "py_voucher_hrs": "Previous year voucher hours. Typically empty or 0",
    "py_voucher_qty": "Previous year voucher quantity. Typically empty or 0",
    "py_shop_rate": "Previous year shop rate. Typically empty or 0",
    "py_actual_hours": "Previous year actual hours",
    "py_total_conversion_ytd_unit_cost": "Previous year total conversion year-to-date unit cost. Typically empty or 0",
    "py_total_conversion_ytd_ext_cost": "Previous year total conversion year-to-date extended cost. Typically empty or 0",
    "attribute1": "Additional attribute 1",
    "attribute2": "Additional attribute 2",
    "attribute3": "Additional attribute 3",
    "attribute4": "Additional attribute 4",
    "attribute5": "Additional attribute 5",
    "attribute6": "Additional attribute 6",
    "attribute7": "Additional attribute 7",
    "attribute8": "Additional attribute 8",
    "attribute9": "Additional attribute 9",
    "attribute10": "Additional attribute 10",
    "source_update_ts": "Source update timestamp",
    "updating_job_name": "Updating job name",
    "source_id": "Source identifier",
    "dl_update_ts": "Data load update timestamp",
    "table_key": "Table key",
    "baseline_hrs_pc_opr": "Baseline hours per operation",
    "baseline_hrs_pc_ce": "Baseline hours per cost element",
    "baseline_hrs_pc_prt": "Baseline hours per part",
    "baseline_opr": "Baseline operation",
    "baseline_ce": "Baseline cost element",
    "baseline_prt": "Baseline part",
    "cy_sso_hrs_pc": "Current year SSO hours per cost element",
    "cy_opr_hrs_pc": "Current year operation hours per cost element",
    "cy_detail_part_extended_cost": "Current year detail part extended cost",
    "py_detail_part_extended_cost": "Previous year detail part extended cost",
    "scrap_equivalent_units": "Scrap equivalent units for the given month. avoid if possible",
    "net_equivalent_units": "Net equivalent units for the given month. avoid if possible",
    "dtl_data_source_id": "Detail data source identifier",
    "plant_code_desc": "Description of the plant code",
    "part_family": "Part family"

    12. How to use conversion dashboard table:

    1. Use the cy_input_cost, cy_voucher_hrs, and cy_voucher_qty, scrap_equivalent_units, net_equivalent_units for calculations.
    2. The total qty for a given month, part, plant combination is the sum of cy_voucher_qty. Same goes for any other combination like operation number, part, plant, month etc.
    3. Net equivalent qty is net_equivalent_units which is used for cost calculations. It is (total - scrap qty).
    4. Scrap units is scrap_equivalent_units column.
    5. hours per piece can be found by sum(cy_voucher_hrs)/sum(net_equivalent_units)
    6. Use year_month column to filter for any month
    7. Use operation_number column to filter on an operation
    8. Use cost_element_description column to filter for type of cost element (first run, rework, etc)
    9. net_equivalent_units remains the same for all given calculations as denominator for a given month.

    
13. spec_details table column definitions:
    
    "specs": "Part Specification",
    "description": "Description of the specification",
    "part_number": "Unique identifier for the part number",
    "engine_model": "Model of the engine the part is used in",
    "design_risk_score": "Risk score associated with the design of the part",
    "title": "Title or name of the part",
    "l1_part_family_desc": "Level 1 part family description",
    "l2_part_family_desc": "Level 2 part family description",
    "l3_part_family_desc": "Level 3 part family description",
    "l4_part_family_desc": "Level 4 part family description",
    "supplier_id": "Unique identifier for the supplier",
    "supplier_nm": "Name of the supplier",
    "supplier_country_cd": "Country code of the supplier",
    "latest_schedule_yr": "Latest scheduled year for the part. Not to be used from this table",
    "pa_order_qty": "Purchase order quantity. Not to be used from this table"

14. Some information on how to read specifications from spec_table:

    "A50TF": "Non-Metallic Materials Spec",
    "B50TF": "Metallic Materials Spec",
    "C50TF": "Metallics Materials Spec",
    "D50TF": "Ancillary Materials Spec",
    "E50TF": "Testing Spec",
    "F50TF": "Finishes Spec",
    "PXXTFXX": "Processes and Inspection Spec",
    "EMPIS": "GE Corporate Specs",
    "AMS": "SAE Aerospace Material Specs",
    "Mil, Others": "Mil & Others Spec"

    Some Few Shot examples for Query Generation follow these:
    1. CMS_input_material:
                Question : Calculate the average unit price for a given part, vendor/shop, and cost period month from material input table, neglecting the MPHE cost.
        Answer:
        SELECT 
            vendor_number,
            vendor_description,
            buc_code_for_2nd_class_billing,
            buc_description,
            part_number,
            cost_period_month,
            SUM(transaction_cost__extended_uc_) / SUM(material_in_quantity) AS avg_unit_price
        FROM 
            cms_input_material_table
        GROUP BY 
            vendor_number, 
            vendor_description, 
            buc_code_for_2nd_class_billing, 
            buc_description, 
            part_number, 
            cost_period_month;
            
        Question : Calculate the average unit price for a given part, vendor/shop, and cost period month from material input table, considering the MPHE cost.
        Answer:
        SELECT 
            vendor_number,
            vendor_description,
            buc_code_for_2nd_class_billing,
            buc_description,
            part_number,
            cost_period_month,
            trans_quantity*unit_mphe_cost AS mphe_cost
            mphe_cost+transaction_cost__extended_uc_ AS total_trans_cost_including_mphe
            SUM(total_trans_cost_including_mphe) / SUM(material_in_quantity) AS avg_unit_price_including_mphe
        FROM 
            cms_input_material_table
        GROUP BY 
            vendor_number, 
            vendor_description, 
            buc_code_for_2nd_class_billing, 
            buc_description, 
            part_number, 
            cost_period_month;

        Question : which supplier saw a step up in unit price for LEAP engine line in 2024?
        Answer : 
        WITH leap_data AS (
            SELECT 
                vendor_number,
                vendor_description,
                buc_code_for_2nd_class_billing,
                buc_description,
                cost_period_month,
                SUM(transaction_cost__extended_uc_) AS total_transaction_cost,
                SUM(material_in_quantity) AS total_material_in_quantity
            FROM 
                your_table_name
            WHERE 
                product_line IN ('GS', 'GT', 'GR') 
                AND substr(cast(cost_period_month as text), 1, 4) = '2024'
                AND ae_cost_element = '52'
            GROUP BY 
                vendor_number,
                vendor_description,
                buc_code_for_2nd_class_billing,
                buc_description,
                cost_period_month
        ),
        average_unit_price AS (
            SELECT 
                vendor_number,
                vendor_description,
                buc_code_for_2nd_class_billing,
                buc_description,
                cost_period_month,
                total_transaction_cost / total_material_in_quantity AS avg_unit_price
            FROM 
                leap_data
        )
        SELECT 
            vendor_number,
            vendor_description,
            buc_code_for_2nd_class_billing,
            buc_description,
            cost_period_month,
            avg_unit_price,
            LAG(avg_unit_price) OVER (PARTITION BY vendor_number, vendor_description, buc_code_for_2nd_class_billing, buc_description ORDER BY cost_period_month) AS prev_avg_unit_price,
            CASE 
                WHEN avg_unit_price > LAG(avg_unit_price) OVER (PARTITION BY vendor_number, vendor_description, buc_code_for_2nd_class_billing, buc_description ORDER BY cost_period_month) THEN 'Step Up'
                ELSE 'No Change'
            END AS price_change
        FROM 
            average_unit_price
        ORDER BY 
            vendor_number,
            vendor_description,
            buc_code_for_2nd_class_billing,
            buc_description,
            cost_period_month;


        Question : Which suppliers had most amount of extra material cost transactions in 2024?
        Answer :
        WITH extra_material_costs AS (
            SELECT 
                vendor_number,
                vendor_description,
                buc_code_for_2nd_class_billing,
                buc_description,
                COUNT(*) AS transaction_count
            FROM 
                your_table_name
            WHERE 
                substr(cast(cost_period_month as text), 1, 4) = '2024'
                AND ae_cost_element = '87'
            GROUP BY 
                vendor_number,
                vendor_description,
                buc_code_for_2nd_class_billing,
                buc_description
        )
        SELECT 
            vendor_number,
            vendor_description,
            buc_code_for_2nd_class_billing,
            buc_description,
            transaction_count
        FROM 
            extra_material_costs
        ORDER BY 
            transaction_count DESC;

        Question : Which suppliers had most amount of total extra material cost in 2024?
        Answer: 
        WITH extra_material_costs AS (
            SELECT 
                vendor_number,
                vendor_description,
                buc_code_for_2nd_class_billing,
                buc_description,
                SUM(transaction_cost__extended_uc_) AS total_transaction_cost
            FROM 
                your_table_name
            WHERE 
                substr(cast(cost_period_month as text), 1, 4) = '2024'
                AND ae_cost_element = '87'
            GROUP BY 
                vendor_number,
                vendor_description,
                buc_code_for_2nd_class_billing,
                buc_description
        )
        SELECT 
            vendor_number,
            vendor_description,
            buc_code_for_2nd_class_billing,
            buc_description,
            total_transaction_cost
        FROM 
            extra_material_costs
        ORDER BY 
            total_transaction_cost DESC;

        Question : Which suppliers had maximum total LOT charges for 2024?
        Answer:
        WITH lot_charges AS (
            SELECT 
                vendor_number,
                vendor_description,
                buc_code_for_2nd_class_billing,
                buc_description,
                part_number,
                description,
                SUM(transaction_cost__extended_uc_) AS total_lot_charges
            FROM 
                your_table_name
            WHERE 
                substr(cast(cost_period_month as text), 1, 4) = '2024'
                AND suffix_code = 'LOT' -- Using suffix_code for LOT charges
            GROUP BY 
                vendor_number,
                vendor_description,
                buc_code_for_2nd_class_billing,
                buc_description,
                part_number,
                description
        )
        SELECT 
            vendor_number,
            vendor_description,
            buc_code_for_2nd_class_billing,
            buc_description,
            part_number,
            description,
            total_lot_charges
        FROM 
            lot_charges
        ORDER BY 
            total_lot_charges DESC;

        Question : What are my farmout expense for different suppliers and parts for 2024?
        Answer:
        WITH farmout_charges AS (
            SELECT 
                vendor_number,
                vendor_description,
                buc_code_for_2nd_class_billing,
                buc_description,
                part_number,
                description,
                SUM(transaction_cost__extended_uc_) AS total_farmout_charges
            FROM 
                your_table_name
            WHERE 
                substr(cast(cost_period_month as text), 1, 4) = '2024'
                AND suffix_code = 'F/O' -- Using suffix_code for farmout charges
            GROUP BY 
                vendor_number,
                vendor_description,
                buc_code_for_2nd_class_billing,
                buc_description,
                part_number,
                description
        )
        SELECT 
            vendor_number,
            vendor_description,
            buc_code_for_2nd_class_billing,
            buc_description,
            part_number,
            description,
            total_farmout_charges
        FROM 
            farmout_charges
        ORDER BY 
            total_farmout_charges DESC;



        Question : Which parts for LEAP are coming from affiliate shops?
        Answer :
        SELECT 
            part_number,
            description,
            buc_code_for_2nd_class_billing,
            buc_description
        FROM your_table_name
        WHERE product_line IN ('GS', 'GT', 'GR')
        AND cost_period_month LIKE '2024%'
        AND vendor_number IS NULL
        AND vendor_description IS NULL
        AND buc_code_for_2nd_class_billing IS NOT NULL
        AND buc_description IS NOT NULL;


        Question : which suppliers or affiliate shops had reverse transactions and what amount in 2024?
        Answer:
        SELECT 
            CASE 
                WHEN vendor_number IS NOT NULL AND vendor_description IS NOT NULL THEN vendor_description
                WHEN vendor_number IS NULL AND vendor_description IS NULL AND buc_code_for_2nd_class_billing IS NOT NULL AND buc_description IS NOT NULL THEN buc_description
                ELSE 'Unknown'
            END AS supplier_name,
            SUM(transaction_cost__extended_uc_) AS total_reverse_amount
        FROM your_table_name
        WHERE product_line IN ('GS', 'GT', 'GR')
        AND cost_period_month LIKE '2024%'
        AND trans_quantity < 0
        GROUP BY supplier_name
        ORDER BY total_reverse_amount DESC;

        Question : Calculate the average unit price for part 737M1687G01, from FADEC, for Jan 2024 from material input table
        Answer:
        SELECT 
            vendor_number,
            vendor_description,
            buc_code_for_2nd_class_billing,
            buc_description,
            part_number,
            cost_period_month,
            SUM(transaction_cost__extended_uc_) / SUM(material_in_quantity) AS avg_unit_price
        FROM 
            cms_input_material_table
        WHERE
            (part_number like '737M1687G%') and (vendor_description like 'FADEC%')
        GROUP BY 
            vendor_number, 
            vendor_description, 
            buc_code_for_2nd_class_billing, 
            buc_description, 
            part_number, 
            cost_period_month;

        Question : What is the monthly trend for 737M1687G01 in CMS input material data. Give me separate values for unit input cost and MPHE.
        Answer :
        SELECT 
            cost_period_month AS cost_period,
            SUBSTR(CAST(cost_period_month AS TEXT), 1, 4) || '-' || SUBSTR(CAST(cost_period_month AS TEXT), 5, 2) AS year_month,
            part_number,
            description AS part_description,
            product_line,
            vendor_number,
            vendor_description,
            ROUND(AVG(unit_input_cost), 2) AS avg_unit_input_cost,
            ROUND(AVG(unit_mphe_cost), 2) AS avg_unit_mphe_cost,
            ROUND(AVG(average_unit_cost), 2) AS avg_total_unit_cost,
            SUM(material_in_quantity) AS total_quantity,
            ROUND(SUM(transaction_cost__extended_uc_), 2) AS total_transaction_cost
        FROM CMS_input_material
        WHERE part_number like '737M1687G%'
            AND cost_period_month BETWEEN 202401 AND 202412
        GROUP BY cost_period_month, part_number, description, product_line, vendor_number, vendor_description
        ORDER BY cost_period_month;



        Question : Which suppliers had most amount of total extra material cost in 2024 February?
        Answer: 
        WITH extra_material_costs AS (
            SELECT 
                vendor_number,
                vendor_description,
                buc_code_for_2nd_class_billing,
                buc_description,
                SUM(transaction_cost__extended_uc_) AS total_transaction_cost
            FROM 
                your_table_name
            WHERE 
                substr(cast(cost_period_month as text), 1, 6) = '202402'
                AND ae_cost_element = '87'
            GROUP BY 
                vendor_number,
                vendor_description,
                buc_code_for_2nd_class_billing,
                buc_description
        )
        SELECT 
            vendor_number,
            vendor_description,
            buc_code_for_2nd_class_billing,
            buc_description,
            total_transaction_cost
        FROM 
            extra_material_costs
        ORDER BY 
            total_transaction_cost DESC;


      2. Publish_Layer


        Question: What is my total spend for this year on various commodities?
Answer:
SELECT 
    commodity_nm,
    SUM(schedule_spend_amt) AS total_spend
FROM 
    Publish_Layer
WHERE 
    schedule_yr = YEAR(CURRENT_DATE) AND
    schedule_type_cd = 'Received'
GROUP BY 
    commodity_nm;
    
Question : What are my top suppliers in terms of total spend in GMC commodity?
Answer : 
SELECT 
    supplier_nm,
    SUM(schedule_spend_amt) AS total_spend
FROM 
    Publish_Layer
WHERE 
    commodity_nm = 'GMC'
GROUP BY 
    supplier_nm
ORDER BY 
    total_spend DESC;
    
Question : What are the parts provided by FADEC?
Answer: 
SELECT 
    part_nbr,
    part_desc
FROM 
    Publish_Layer
WHERE 
    supplier_id = (
        SELECT 
            supplier_id
        FROM 
            Publish_Layer
        WHERE 
            LOWER(supplier_nm) LIKE LOWER('%FADEC%')
        LIMIT 1
    );

Question: what are my suppliers which saw maximum inflation compared to previous year?
Answer:
SELECT 
    supplier_id,
    supplier_nm,
    unit_price_current_year,
    unit_price_previous_year,
    ((unit_price_current_year - unit_price_previous_year) / unit_price_previous_year) * 100 AS inflation_percentage
FROM (
    SELECT 
        supplier_id,
        supplier_nm,
        SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_spend_amt ELSE 0 END) / SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS unit_price_current_year,
        SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_spend_amt ELSE 0 END) / SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS unit_price_previous_year
    FROM 
        Publish_Layer
    GROUP BY 
        supplier_id, supplier_nm
) AS spend_data
ORDER BY 
    inflation_percentage DESC;


Question: what are my suppliers which saw maximum deflation compared to previous year?
Answer:
SELECT 
    supplier_id,
    supplier_nm,
    unit_price_current_year,
    unit_price_previous_year,
    ((unit_price_previous_year - unit_price_current_year) / unit_price_previous_year) * 100 AS deflation_percentage
FROM (
    SELECT 
        supplier_id,
        supplier_nm,
        SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_spend_amt ELSE 0 END) / SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS unit_price_current_year,
        SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_spend_amt ELSE 0 END) / SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS unit_price_previous_year
    FROM 
        Publish_Layer
    GROUP BY 
        supplier_id, supplier_nm
) AS spend_data
ORDER BY 
    deflation_percentage DESC;



Question : which commodities saw maximum productivity compared to previous year?
(Productivity is how much less we have spent compared to last year. The lesser we spent, the better the productivity)
Answer:
SELECT 
    commodity_nm,
    unit_price_current_year,
    unit_price_previous_year,
    ((unit_price_previous_year - unit_price_current_year) / unit_price_previous_year) * 100 AS productivity_percentage
FROM (
    SELECT 
        commodity_nm,
        SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_spend_amt ELSE 0 END) / SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS unit_price_current_year,
        SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_spend_amt ELSE 0 END) / SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS unit_price_previous_year
    FROM 
        Publish_Layer
    GROUP BY 
        commodity_nm
) AS spend_data
ORDER BY 
    productivity_percentage DESC;



Question: which part saw maximum inflation in terms of absolute dollar value from last year?
Answer:
SELECT 
    part_nbr,
    part_desc,
    unit_price_current_year,
    unit_price_previous_year,
    (unit_price_current_year - unit_price_previous_year) AS inflation_value
FROM (
    SELECT 
        part_nbr,
        part_desc,
        SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_spend_amt ELSE 0 END) / SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS unit_price_current_year,
        SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_spend_amt ELSE 0 END) / SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS unit_price_previous_year
    FROM 
        Publish_Layer
    GROUP BY 
        part_nbr, part_desc
) AS spend_data
ORDER BY 
    inflation_value DESC
LIMIT 1;


Question : which commodities saw maximum absolute productivity in terms of dollars compared to previous year?
Answer :
SELECT 
    commodity_nm,
    unit_price_current_year,
    unit_price_previous_year,
    (unit_price_previous_year - unit_price_current_year) AS absolute_productivity_value
FROM (
    SELECT 
        commodity_nm,
        SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_spend_amt ELSE 0 END) / SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS unit_price_current_year,
        SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_spend_amt ELSE 0 END) / SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS unit_price_previous_year
    FROM 
        Publish_Layer
    GROUP BY 
        commodity_nm
) AS spend_data
ORDER BY 
    absolute_productivity_value DESC;


Question : What are LEAP suppliers located in USA?
Answer:
SELECT 
    supplier_id,
    supplier_nm,
    supplier_country_cd,
    supplier_state_cd
FROM 
    Publish_Layer
WHERE 
    engine_family_cd = 'LEAP' AND
    supplier_country_cd = 'US';

Question : what commodities does TEI provide?
Answer : 
SELECT 
    commodity_nm
FROM 
    Publish_Layer
WHERE 
    supplier_nm LIKE '%TEI%'
GROUP BY 
    commodity_nm;


Question : How much am I going to spend this year on different commodities for leap?
Answer:
SELECT 
    commodity_nm,
    SUM(schedule_spend_amt) AS total_spend
FROM 
    Publish_Layer
WHERE 
    engine_family_cd = 'LEAP' AND
    schedule_type_cd = 'Scheduled' AND
    schedule_yr = YEAR(CURRENT_DATE)
GROUP BY 
    commodity_nm;


Question : which suppliers have PAs ending this year and what are the respective part number and commodities for those PAs?
Answer :
SELECT 
    supplier_id,
    supplier_nm,
    part_nbr,
    commodity_nm,
    pa_place_end_dt
FROM 
    Publish_Layer
WHERE 
    YEAR(pa_place_end_dt) = YEAR(CURRENT_DATE);


Question: Which part numbers and supplier combination showed a step up in unit price last year when compared month over month?
Answer:
WITH monthly_prices AS (
    SELECT 
        part_nbr,
        supplier_id,
        supplier_nm,
        schedule_mo,
        SUM(schedule_spend_amt) / SUM(schedule_qty) AS unit_price
    FROM 
        Publish_Layer
    WHERE 
        schedule_yr = 2024 AND
        schedule_type_cd = 'Received'
    GROUP BY 
        part_nbr, supplier_id, supplier_nm, schedule_mo
),
price_changes AS (
    SELECT 
        part_nbr,
        supplier_id,
        supplier_nm,
        schedule_mo,
        unit_price,
        LAG(unit_price) OVER (PARTITION BY part_nbr, supplier_id ORDER BY schedule_mo) AS previous_month_price
    FROM 
        monthly_prices
)
SELECT 
    part_nbr,
    supplier_id,
    supplier_nm,
    schedule_mo,
    unit_price,
    previous_month_price,
    (unit_price - previous_month_price) AS price_increase
FROM 
    price_changes
WHERE 
    unit_price > previous_month_price
ORDER BY 
    price_increase DESC;


Question : Give me all Shared Hardware Solutions (SHS) parts having only single source
Answer:
SELECT 
    part_nbr,
    part_desc,
    COUNT(DISTINCT supplier_id) AS supplier_count
FROM 
    Publish_Layer
WHERE 
    LOWER(commodity_nm) = LOWER('Shared Hardware Solutions')
GROUP BY 
    part_nbr, part_desc
HAVING 
    COUNT(DISTINCT supplier_id) = 1;

Question : what is the difference in cy vs py volume (qty) for GMC for LEAP?
Answer: 
SELECT 
    SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS current_year_qty,
    SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS previous_year_qty,
    SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) - 
    SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS qty_difference
FROM 
    Publish_Layer
WHERE 
    commodity_nm = 'GMC' AND
    engine_family_cd = 'LEAP';

Question : What are the best performing suppliers in terms of productivity for LEAP?
Answer: 
SELECT 
    supplier_id,
    supplier_nm,
    unit_price_current_year,
    unit_price_previous_year,
    ((unit_price_previous_year - unit_price_current_year) / unit_price_previous_year) * 100 AS productivity_percentage,
    total_spend_current_year - total_spend_previous_year AS total_spend_delta
FROM (
    SELECT 
        supplier_id,
        supplier_nm,
        SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_spend_amt ELSE 0 END) AS total_spend_current_year,
        SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_spend_amt ELSE 0 END) AS total_spend_previous_year,
        SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_spend_amt ELSE 0 END) / SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS unit_price_current_year,
        SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_spend_amt ELSE 0 END) / SUM(CASE WHEN schedule_yr = YEAR(CURRENT_DATE) - 1 AND schedule_type_cd = 'Received' THEN schedule_qty ELSE 0 END) AS unit_price_previous_year
    FROM 
        Publish_Layer
    WHERE 
        engine_family_cd = 'LEAP'
    GROUP BY 
        supplier_id, supplier_nm
) AS spend_data
ORDER BY 
    productivity_percentage DESC;




      3. ternd_report_gnex_leap table

                Question : For LEAP, what are my top 10 parts for nov 2024?
        Answer:
        SELECT part_number, part_description, act_total_set_cost
        FROM your_table_name
        WHERE engine IN ('LEAP 1A', 'LEAP 1B')
        AND month_name = 'Nov'
        AND cost_period = '202411'
        ORDER BY act_total_set_cost DESC
        LIMIT 10;


        Question : For LEAP, what are my top 10 buy parts for nov 2024?
        Answer:
        SELECT part_number, part_description, act_total_set_cost
        FROM your_table_name
        WHERE engine IN ('LEAP 1A', 'LEAP 1B')
        AND month_name = 'Nov'
        AND cost_period = '202411'
        AND value_stream = 'Unallocated Sourcing Prime'
        ORDER BY act_total_set_cost DESC
        LIMIT 10;

        Question : Which buy parts for L1A show month over month highest inflation in AUC for 2024 in terms of absolute dollar value?
        Answer : 
        WITH monthly_costs AS (
            SELECT 
                part_number, 
                part_description, 
                month_name, 
                cost_period, 
                act_total_set_cost,
                LAG(act_total_set_cost) OVER (PARTITION BY part_number ORDER BY cost_period) AS previous_month_cost
            FROM your_table_name
            WHERE engine = 'LEAP 1A'
            AND value_stream = 'Unallocated Sourcing Prime'
            AND cost_period LIKE '2024%'
        ),
        inflation AS (
            SELECT 
                part_number, 
                part_description, 
                (act_total_set_cost - previous_month_cost) AS monthly_diff
            FROM monthly_costs
            WHERE previous_month_cost IS NOT NULL
        ),
        total_inflation AS (
            SELECT 
                part_number, 
                part_description, 
                SUM(monthly_diff) AS total_inflation_value
            FROM inflation
            GROUP BY part_number, part_description
        )
        SELECT 
            part_number, 
            part_description, 
            total_inflation_value
        FROM total_inflation
        ORDER BY total_inflation_value DESC
        LIMIT 1;

        Question: Which parts in L1B had maximum average material set cost last year?
        Answer:
        WITH last_year_data AS (
            SELECT 
                part_number, 
                part_description, 
                act_mtl_set_cost
            FROM your_table_name
            WHERE engine = 'LEAP 1B'
            AND cost_period LIKE CONCAT(YEAR(CURDATE()) - 1, '%')
        ),
        average_material_cost AS (
            SELECT 
                part_number, 
                part_description, 
                AVG(act_mtl_set_cost) AS avg_material_set_cost
            FROM last_year_data
            GROUP BY part_number, part_description
        )
        SELECT 
            part_number, 
            part_description, 
            avg_material_set_cost
        FROM average_material_cost
        ORDER BY avg_material_set_cost DESC
        LIMIT 1;

        Question: What are my top 5 parts for leap 1a on the basis of contribution to the engine AUC?

        WITH engine_auc AS (
            SELECT SUM(act_total_set_cost) AS total_engine_auc
            FROM trend_report_genx_leap
            WHERE engine = 'LEAP 1A'
            AND cost_period = 202412
        )
        SELECT 
            t.part_number,
            t.part_description,
            t.value_stream,
            t.act_total_set_cost,
            (t.act_total_set_cost / e.total_engine_auc) * 100 AS percentage_of_auc
        FROM 
            trend_report_genx_leap t,
            engine_auc e
        WHERE 
            t.engine = 'LEAP 1A'
            AND t.cost_period = 202412
        ORDER BY 
            t.act_total_set_cost DESC
        LIMIT 5;



      4. Part_Scorecard

                Question : what was the shop output auc for 2025 Jan for 2552M06G05 from wilmington for LEAP?
        Answer :
        SELECT 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num,
            SUM(cy_ext_total_output_cst) / SUM(cy_ship_quantity) AS shop_output_auc
        FROM 
            part_scorecard
        WHERE 
            plant_code = 'WIL' AND
            ship_part_no = '2552M06G05' AND
            year = 2025 AND
            month_name = 'Jan' AND
            engine_family like 'LEAP%'
        GROUP BY 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num;

        Question : what was the shop output conversion auc for 2025 Jan for 2552M06G05 from wilmington?
        Answer :
        WITH monthly_total_qty AS (
            SELECT 
                SUM(cy_ship_quantity) AS total_qty
            FROM 
                part_scorecard
            WHERE 
                plant_code = 'WIL' AND
                ship_part_no = '2552M06G05' AND
                year = 2025 AND
                month_name = 'Jan'
        )
        SELECT 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num,
            cost_element_cd_sprs,
            SUM(cy_ext_total_output_cst) / (SELECT total_qty FROM monthly_total_qty) AS conversion_auc
        FROM 
            part_scorecard
        WHERE 
            plant_code = 'WIL' AND
            ship_part_no = '2552M06G05' AND
            year = 2025 AND
            month_name = 'Jan' AND
            cost_element_cd_sprs = 'CONVERSION'
        GROUP BY 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num,
            cost_element_cd_sprs;

        Question: Question : what was the shop output farmout auc for 2025 Jan for 2552M06G05 from wilmington?
        Answer:
        WITH monthly_total_qty AS (
            SELECT 
                SUM(cy_ship_quantity) AS total_qty
            FROM 
                part_scorecard
            WHERE 
                plant_code = 'WIL' AND
                ship_part_no = '2552M06G05' AND
                year = 2025 AND
                month_name = 'Jan'
        )
        SELECT 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num,
            cost_element_cd_sprs,
            SUM(cy_ext_total_output_cst) / (SELECT total_qty FROM monthly_total_qty) AS farmout_auc
        FROM 
            part_scorecard
        WHERE 
            plant_code = 'WIL' AND
            ship_part_no = '2552M06G05' AND
            year = 2025 AND
            month_name = 'Jan' AND
            cost_element_cd_sprs = 'OV/FARMOUT'
        GROUP BY 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num,
            cost_element_cd_sprs;

        Question: How many 2552M06G05 parts were shipped from wilmington in jan 2025?
        Answer : 
        SELECT 
            SUM(cy_ship_quantity) AS total_shipped_quantity
        FROM 
            part_scorecard
        WHERE 
            plant_code = 'WIL' AND
            ship_part_no = '2552M06G05' AND
            year = 2025 AND
            month_name = 'Jan';

        Question : What are the detail parts that go into 2552M06G05?
        Answer:
        SELECT 
            detail_part_no,
            detail_part_description
        FROM 
            part_scorecard
        WHERE 
            ship_part_no = '2552M06G05';

        Question : what was the shop output scrap auc for 2025 Jan for 2552M06G05 from wilmington?
        Answer:
        WITH monthly_total_qty AS (
            SELECT 
                SUM(cy_ship_quantity) AS total_qty
            FROM 
                part_scorecard
            WHERE 
                plant_code = 'WIL' AND
                ship_part_no = '2552M06G05' AND
                year = 2025 AND
                month_name = 'Jan'
        )
        SELECT 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num,
            cost_element_description,
            SUM(cy_ext_total_output_cst) / (SELECT total_qty FROM monthly_total_qty) AS scrap_auc
        FROM 
            part_scorecard
        WHERE 
            plant_code = 'WIL' AND
            ship_part_no = '2552M06G05' AND
            year = 2025 AND
            month_name = 'Jan' AND
            cost_element_description = 'SCRAP'
        GROUP BY 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num,
            cost_element_description;

        Question : what cost elements I have within losses? what were the auc for them for jan 2025 for 2552M06G05 from wilmington?
        Answer : 
        WITH monthly_total_qty AS (
            SELECT 
                SUM(cy_ship_quantity) AS total_qty
            FROM 
                part_scorecard
            WHERE 
                plant_code = 'WIL' AND
                ship_part_no = '2552M06G05' AND
                year = 2025 AND
                month_name = 'Jan'
        )
        SELECT 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num,
            cost_element_description,
            SUM(cy_ext_total_output_cst) / (SELECT total_qty FROM monthly_total_qty) AS auc
        FROM 
            part_scorecard
        WHERE 
            plant_code = 'WIL' AND
            ship_part_no = '2552M06G05' AND
            year = 2025 AND
            month_name = 'Jan' AND
            cost_element_cd_sprs = 'LOSSES'
        GROUP BY 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num,
            cost_element_description;


        Question :  give me the part shop auc trend for 2024 for 2552M06G05 from wilmington
        Answer :
        WITH monthly_total_qty AS (
            SELECT 
                year,
                month_name,
                SUM(cy_ship_quantity) AS total_qty
            FROM 
                part_scorecard
            WHERE 
                year = 2024
            GROUP BY 
                year,
                month_name
        )
        SELECT 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num,
            SUM(cy_ext_total_output_cst) / monthly_total_qty.total_qty AS shop_output_auc
        FROM 
            part_scorecard
        JOIN 
            monthly_total_qty
        ON 
            part_scorecard.year = monthly_total_qty.year AND
            part_scorecard.month_name = monthly_total_qty.month_name
        WHERE 
            year = 2024
        GROUP BY 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num,
            monthly_total_qty.total_qty
        ORDER BY 
            year,
            month_num;

        Question : what are the parts bieng made in greenville shop?
        Answer : 
        SELECT DISTINCT    ship_part_no,    ship_part_description
        FROM    part_scorecard
        WHERE    plant_code = 'GRN'
        ORDER BY    ship_part_no;


        Question : what was the percentage share split of quantity between AUB and GRN shops for 2024 december for given number?
        Answer : 
        WITH total_quantity AS (
            SELECT SUM(cy_ship_quantity) AS total_qty
            FROM Part_Scorecard
            WHERE ship_part_no = '2747M92P01'
            AND year = 2024
            AND month_name = 'Dec'
        )
        SELECT 
            plant_code,
            plant_name,
            ship_part_no,
            year,
            month_name,
            SUM(cy_ship_quantity) AS quantity,
            (SELECT total_qty FROM total_quantity) AS total_quantity,
            ROUND(SUM(cy_ship_quantity) * 100.0 / (SELECT total_qty FROM total_quantity), 2) AS percentage_share
        FROM 
            Part_Scorecard
        WHERE 
            ship_part_no = '2747M92P01'
            AND year = 2024
            AND month_name = 'Dec'
        GROUP BY 
            plant_code,
            plant_name,
            ship_part_no,
            year,
            month_name
        ORDER BY 
            plant_code;

        Question : Top 10 parts in terms of shop output auc from wilmington in jan 2025?
        Answer :
        SELECT 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num,
            SUM(cy_ext_total_output_cst) / SUM(cy_ship_quantity) AS shop_output_auc
        FROM 
            part_scorecard
        WHERE 
            plant_code = 'WIL' AND
            year = 2025 AND
            month_name = 'Jan'
        GROUP BY 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num
        ORDER BY 
            shop_output_auc DESC
        LIMIT 10;

        Question : Top 10 parts in terms of shop output auc from wilmington in jan 2025 for leap 1a?
        Answer:
        SELECT 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num,
            SUM(cy_ext_total_output_cst) / SUM(cy_ship_quantity) AS shop_output_auc
        FROM 
            part_scorecard
        WHERE 
            plant_code = 'WIL' AND
            year = 2025 AND
            month_name = 'Jan' AND
            LOWER(engine_family) LIKE '%leap%1a%'
        GROUP BY 
            plant_code,
            plant_name,
            ship_part_no,
            ship_part_description,
            engine_family,
            year,
            month_name,
            month_num
        ORDER BY 
            shop_output_auc DESC
        LIMIT 10;




        5. Conversion Dashboard:
        
                        Question : 2085M36P03 give me the hours per piece trend in 2024.
        Answer : 
        SELECT 
            reporting_year AS Year,
            reporting_month AS Month,
            month_name AS Month_Name,
            SUM(cy_voucher_hrs) / SUM(net_equivalent_units) AS Hours_per_Piece
        FROM 
            Conversion_dashboard
        WHERE 
            part_number = '2085M36P03'
            AND reporting_year = 2024
        GROUP BY 
            reporting_year, reporting_month, month_name
        ORDER BY 
            reporting_month;


        Question : 2085M36P03 give me a breakup of hours per piece terms for cost elements in jan 2025.
        Answer :
        WITH total_units AS (
            SELECT SUM(net_equivalent_units) as total_net_units
            FROM Conversion_dashboard
            WHERE part_number = '2085M36P03'
            AND reporting_year = 2025
            AND month_name = 'Jan'
        )
        SELECT 
            cd.part_number,
            cd.cost_element_description,
            SUM(cd.cy_voucher_hrs) as total_hours,
            tu.total_net_units,
            SUM(cd.cy_voucher_hrs) / tu.total_net_units as hours_per_piece
        FROM 
            Conversion_dashboard cd,
            total_units tu
        WHERE 
            cd.part_number = '2085M36P03'
            AND cd.reporting_year = 2025
            AND cd.month_name = 'Jan'
        GROUP BY 
            cd.part_number,
            cd.cost_element_description,
            tu.total_net_units
        ORDER BY 
            hours_per_piece DESC;

        Question : 2085M36P03 give me the first run labor hours per piece for jan 2025.
        Answer:
        WITH total_units AS (
            SELECT SUM(net_equivalent_units) as total_net_units
            FROM Conversion_dashboard
            WHERE part_number = '2085M36P03'
            AND reporting_year = 2025
            AND month_name = 'Jan'
        )
        SELECT 
            cd.part_number,
            cd.cost_element_description,
            SUM(cd.cy_voucher_hrs) as total_hours,
            tu.total_net_units,
            SUM(cd.cy_voucher_hrs) / tu.total_net_units as hours_per_piece
        FROM 
            Conversion_dashboard cd,
            total_units tu
        WHERE 
            cd.part_number = '2085M36P03'
            AND cd.reporting_year = 2025
            AND cd.month_name = 'Jan'
            AND cd.cost_element_description = 'FIRST RUN LABOR'
        GROUP BY 
            cd.part_number,
            cd.cost_element_description,
            tu.total_net_units
        ORDER BY 
            hours_per_piece DESC;


        Question : 2085M36P03 give me the inspection labor hours per piece for jan 2025.
        Answer:
        WITH total_units AS (
            SELECT SUM(net_equivalent_units) as total_net_units
            FROM Conversion_dashboard
            WHERE part_number = '2085M36P03'
            AND reporting_year = 2025
            AND month_name = 'Jan'
        )
        SELECT 
            cd.part_number,
            cd.cost_element_description,
            SUM(cd.cy_voucher_hrs) as total_hours,
            tu.total_net_units,
            SUM(cd.cy_voucher_hrs) / tu.total_net_units as hours_per_piece
        FROM 
            Conversion_dashboard cd,
            total_units tu
        WHERE 
            cd.part_number = '2085M36P03'
            AND cd.reporting_year = 2025
            AND cd.month_name = 'Jan'
            AND cd.cost_element_description = 'INSPECTION LABOR'
        GROUP BY 
            cd.part_number,
            cd.cost_element_description,
            tu.total_net_units
        ORDER BY 
            hours_per_piece DESC;

        6. specs_details table:

                Question : give me a sql query to find all the suppliers for this spec :P3TF2/P3TF47
        Ans
        SELECT supplier_id, supplier_nm, supplier_country_cd
        FROM your_table_name
        WHERE specs = 'P3TF2/P3TF47';

        Question : what are my specs for this part : 1710M96P09?
        Answer : 
        SELECT DISTINCT specs
        FROM your_table_name
        WHERE part_number = '1710M96P09';

        Question : What specs have only a single supplier?
        Answer:
        SELECT  DISTINCT specs
        FROM your_table_name
        GROUP BY specs
        HAVING COUNT(DISTINCT supplier_id) = 1;

        Question : What are my specs for brackets?
        Answer:
        SELECT DISTINCT specs
        FROM your_table_name
        WHERE l2_part_family_desc = 'BRACKET';


    Now, generate the SQL query for the following question asked {question}
    no other text is required other than the query.
    no explaination is required other than the query.

"""


viz_suggestion_template = """
    Analyze the SQL query and its results to recommend an appropriate visualization.

    SQL Query: {query}
    Query Results (first 10 rows): {results}
    Question: {question}

    Return ONLY a valid JSON object with this exact structure:
    {{
      "visualization_type": "bar_chart|line_chart|pie_chart|scatter_plot|table|none",
      "x_axis": "column name for x-axis",
      "y_axis": "column name for y-axis",
      "color_by": "column for color differentiation (optional)",
      "title": "suggested title for the visualization",
      "description": "brief explanation of why this visualization is appropriate"
    }}

    Choose visualization_type based on these guidelines:
    - bar_chart: For comparing categories or showing counts/sums
    - line_chart: For time series or trends
    - pie_chart: For showing proportions of a whole (limit to <10 categories)
    - scatter_plot: For showing relationships between two numeric variables
    - table: For detailed data that's better viewed as a table
    - none: If no visualization is appropriate

    Return ONLY the JSON object and nothing else.
    """
    
response_template = """Based on the table schema, question, sql query, and sql response, 
    write a natural language response
    Make a table as well and always make the full table from the sql data.
    Question: {question}
    SQL Query: {query}
    SQL Response: {response}"""
    
