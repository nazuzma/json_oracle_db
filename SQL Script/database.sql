---------------------------------------------------------------------------------------
-- IMPORTANT!
-- Select the target schema below by uncommenting the right line!
-- WARNING: this will wipeout the entire EM CTL repository!
-- Also ensure to execute the script under the same user (i.e. EM_REPO or EM_REPO_DEV)
---------------------------------------------------------------------------------------
alter session set current_schema = EM_REPO_DEV;
--alter session set current_schema = EM_REPO;
---------------------------------------------------------------------------------------

-drop table a_ccsd_status;
-drop table ATTACHED_FILE;
-drop table A_CCSD cascade constraints;
-drop table B_TESTS cascade constraints;
-drop table C_COMPONENTS cascade constraints;
-drop table D_REINFORCEMENTS cascade constraints;
-drop table E_INDICATORS cascade constraints;
-drop table APPENDIX_FP cascade constraints;
-drop table APPENDIX_RR cascade constraints;
-drop table A_CCSD_EXTRA cascade constraints;
-drop table B_TESTS_EXTRA cascade constraints;
-drop table C_COMPONENTS_EXTRA cascade constraints;
-drop table D_REINFORCEMENTS_EXTRA cascade constraints;
-drop table E_INDICATORS_EXTRA cascade constraints;
-drop table APPENDIX_FP_Extra cascade constraints;
-drop table APPENDIX_RR_Extra cascade constraints;
-drop table ctl cascade constraints;

-drop sequence shared_sequence;

CREATE TABLE A_CCSD
(
    "A_CCSD_ID"                     NUMBER(36) NOT NULL,
    "CRD-revision-side ID"          VARCHAR(50),
    "CRD"                           VARCHAR(50),
    "CRD revision"                  VARCHAR(50),
    "Symmetric"                     VARCHAR(50),
    "Side"                          VARCHAR(50),
    "Origin"                        VARCHAR(50),
    "User"                          VARCHAR(50),
    "Tire size"                     VARCHAR(50),
    "CTC"                           FLOAT(36),
    "CTC revision"                  VARCHAR(50),
    "ERD-ARD"                       VARCHAR(50),
    "Manual version"                VARCHAR(50),
    "Framework version"             FLOAT(36),
    "Design manual"                 VARCHAR(50),
    "Design code"                   VARCHAR(50),
    "OD"                            FLOAT(36),
    "Section width"                 FLOAT(36),
    "PX1"                           FLOAT(36),
    "TWX"                           FLOAT(36),
    "TCW"                           FLOAT(36),
    "Rim flange protector"          VARCHAR(50),
    "EA1"                           FLOAT(36),
    "EA2"                           FLOAT(36),
    "ED1"                           FLOAT(36),
    "ED8"                           FLOAT(36),
    "ED10"                          FLOAT(36),
    "Apex 3 layup"                  VARCHAR(50),
    "ED6"                           FLOAT(36),
    "ED7"                           FLOAT(36),
    "GD1"                           FLOAT(36),
    "GD2"                           FLOAT(36),
    "GD3"                           FLOAT(36),
    "ID0"                           FLOAT(36),
    "ID1"                           FLOAT(36),
    "ID2"                           FLOAT(36),
    "ID3"                           FLOAT(36),
    "ID4"                           FLOAT(36),
    "ID5"                           FLOAT(36),
    "ID6"                           FLOAT(36),
    "ID7"                           FLOAT(36),
    "ID8"                           FLOAT(36),
    "ID9"                           FLOAT(36),
    "ID20"                          FLOAT(36),
    "ID21"                          FLOAT(36),
    "ID22"                          FLOAT(36),
    "ID23"                          FLOAT(36),
    "ID24"                          FLOAT(36),
    "ID25"                          FLOAT(36),
    "ID26"                          FLOAT(36),
    "ID27"                          FLOAT(36),
    "ID28"                          FLOAT(36),
    "ID29"                          FLOAT(36),
    "ID60"                          FLOAT(36),
    "ID61"                          FLOAT(36),
    "ID62"                          FLOAT(36),
    "ID63"                          FLOAT(36),
    "ID64"                          FLOAT(36),
    "ID65"                          FLOAT(36),
    "ID66"                          FLOAT(36),
    "ID67"                          FLOAT(36),
    "ID68"                          FLOAT(36),
    "ID69"                          FLOAT(36),
    "Number of plies"               FLOAT(36),
    "Ply layup"                     VARCHAR(50),
    "EE1"                           FLOAT(36),
    "EE2"                           FLOAT(36),
    "EE3"                           FLOAT(36),
    "EE7"                           FLOAT(36),
    "EE8"                           FLOAT(36),
    "EE9"                           FLOAT(36),
    "EE12"                          FLOAT(36),
    "EE13"                          FLOAT(36),
    "EE14"                          FLOAT(36),
    "EE15"                          FLOAT(36),
    "EE16"                          FLOAT(36),
    "EX2"                           FLOAT(36),
    "Flipper layup"                 VARCHAR(50),
    "EM2"                           FLOAT(36),
    "EM5"                           FLOAT(36),
    "Stiffener inside layup"        VARCHAR(50),
    "EW3"                           FLOAT(36),
    "EW4"                           FLOAT(36),
    "EW7"                           FLOAT(36),
    "EW8"                           FLOAT(36),
    "First chipper layup"           VARCHAR(50),
    "EL1"                           FLOAT(36),
    "EL2"                           FLOAT(36),
    "EL9"                           FLOAT(36),
    "EL11"                          FLOAT(36),
    "EL7"                           FLOAT(36),
    "EL8"                           FLOAT(36),
    "EL12"                          FLOAT(36),
    "EL13"                          FLOAT(36),
    "Toeguard layup"                VARCHAR(50),
    "EB1"                           FLOAT(36),
    "EB2"                           FLOAT(36),
    "EB5"                           FLOAT(36),
    "EB6"                           FLOAT(36),
    "GC11"                          FLOAT(36),
    "GC13"                          FLOAT(36),
    "EF1"                           FLOAT(36),
    "EF3"                           FLOAT(36),
    "GF1"                           FLOAT(36),
    "GF13"                          FLOAT(36),
    "GF31"                          FLOAT(36),
    "GF32"                          FLOAT(36),
    "GF33"                          FLOAT(36),
    "GV10"                          FLOAT(36),
    "GV11"                          FLOAT(36),
    "GV12"                          FLOAT(36),
    "Sidewall layup"                VARCHAR(50),
    "EG1"                           FLOAT(36),
    "EG6"                           FLOAT(36),
    "GG1"                           FLOAT(36),
    "BBD"                           FLOAT(36),
    "BWF"                           FLOAT(36),
    "WN1"                           FLOAT(36),
    "WN2"                           FLOAT(36),
    "GK1"                           FLOAT(36),
    "GK22"                          FLOAT(36),
    "Overlay layup"                 VARCHAR(50),
    "WP1"                           FLOAT(36),
    "WP2"                           FLOAT(36),
    "Tread layup"                   VARCHAR(50),
    "ET21"                          FLOAT(36),
    "ET23"                          FLOAT(36),
    "ET25"                          FLOAT(36),
    "GS0"                           FLOAT(36),
    "GS1"                           FLOAT(36),
    "GS2"                           FLOAT(36),
    "GS43"                          FLOAT(36),
    "GS44 CL"                       FLOAT(36),
    "GS44 SH"                       FLOAT(36),
    "GT1"                           FLOAT(36),
    "GT2"                           FLOAT(36),
    "GT3"                           FLOAT(36),
    "GT4"                           FLOAT(36),
    "Bead configuration"            VARCHAR(50),
    "WC1"                           FLOAT(36),
    PRIMARY KEY ("A_CCSD_ID")
);

CREATE TABLE B_TESTS
(
    "B_TESTS_ID"                    NUMBER(36) NOT NULL,
    "A_CCSD_ID"                     NUMBER(36),
    "Test ID"                       VARCHAR(50),
    "CRD-revision-side ID"          VARCHAR(50),
    "User"                          VARCHAR(50),
    "Type"                          VARCHAR(50),
    "Description"                   VARCHAR(250),
    "CRD"                           VARCHAR(50),
    "CRD revision"                  VARCHAR(50),
    "Folder name"                   VARCHAR(60),
    "Test path"                     VARCHAR(250),
    "Symmetric"                     VARCHAR(50),
    "VTI"                           NUMBER(36),
    "Construction"                  VARCHAR(50),
    "Material model"                VARCHAR(50),
    "DEW version"                   VARCHAR(50),
    "Rolling surface"               VARCHAR(50),
    "Drum diameter (mm)"            FLOAT(36),
    "B&T drum diameter (mm)"        FLOAT(36),
    "Tire mass (kgm)"               FLOAT(36),
    "Vehicle speed (kph)"           FLOAT(36),
    "Cooldown"                      VARCHAR(50),
    "Overlay prestrain"             FLOAT(36),
    "Unit system"                   VARCHAR(50),
    "Rim width (in)"                FLOAT(36),
    "Rim contour"                   VARCHAR(50),
    "Rim diameter (in)"             FLOAT(36),
    "1/2 tread arc width (mm)"      FLOAT(36),
    "1/2 base width (mm)"           FLOAT(36),
    "1/2 section width (mm)"        FLOAT(36),
    "Mold cavity OD"                FLOAT(36),
    "Groove contact"                VARCHAR(50),
    "Sipe contact"                  VARCHAR(50),
    PRIMARY KEY ("B_TESTS_ID"),
    CONSTRAINT "FK_A_B_CCSD_ID" FOREIGN KEY ("A_CCSD_ID") REFERENCES A_CCSD ("A_CCSD_ID") On delete cascade

);

CREATE TABLE C_COMPONENTS
(
    "C_COMPONENTS_ID"               NUMBER(36) NOT NULL,
    "B_TESTS_ID"                    NUMBER(36),
    "Test-component ID"             VARCHAR(50),
    "Test ID"                       VARCHAR(50),
    "Component"                     VARCHAR(50),
    "Compound"                      VARCHAR(50),
    "Sample ID"                     VARCHAR(50),
    "Volume (mm3)"                  FLOAT(36),
    "Density (kg/m3)"               FLOAT(36),
    "Mass (kg)"                     FLOAT(36),
    "Compound density (kg/m3)"      FLOAT(36),
    PRIMARY KEY ("C_COMPONENTS_ID"),
    CONSTRAINT "FK_B_C_TESTS_ID" FOREIGN KEY ("B_TESTS_ID") REFERENCES B_TESTS ("B_TESTS_ID") on delete cascade
);



CREATE TABLE D_REINFORCEMENTS
(
    "D_REINFORCEMENTS_ID"           NUMBER(36) NOT NULL,
    "B_TESTS_ID"                    NUMBER(36),
    "Test-component ID"             VARCHAR(50),
    "Test ID"                       VARCHAR(50),
    "Component"                     VARCHAR(50),
    "Cord code"                     VARCHAR(50),
    "Cord serial"                   VARCHAR(50),
    "Cord density"                  FLOAT(36),
    "Green EPI"                     FLOAT(36),
    "Green angle (deg)"             FLOAT(36),
    "Cured angle (deg)"             FLOAT(36),
    "Green radius (mm)"             FLOAT(36),
    "Cured radius (mm)"             FLOAT(36),
    "Green gauge (mm)"              FLOAT(36),
    "Treatment code"                VARCHAR(50),
    "Creep factor"                  FLOAT(36),
    PRIMARY KEY ("D_REINFORCEMENTS_ID"),
    CONSTRAINT "FK_B_D_TESTS_ID" FOREIGN KEY ("B_TESTS_ID") REFERENCES B_TESTS ("B_TESTS_ID") on delete cascade
);



CREATE TABLE E_INDICATORS
(
    "E_INDICATORS_ID"                NUMBER(36) NOT NULL,
    "B_TESTS_ID"                     NUMBER(36),
    "Test-load-pressure ID"          VARCHAR(50),
    "VTI"                            NUMBER(36),
    "Test ID"                        VARCHAR(50),
    "Pressure (bar)"                 FLOAT(36),
    "Vertical load (kg)"             FLOAT(36),
    "Camber angle (deg)"             FLOAT(36),
    "Section diameter (mm)"          FLOAT(36),
    "Overall diameter (mm)"                        FLOAT(36),
    "CL (mm)"                        FLOAT(36),
    "Width (mm)"                     FLOAT(36),
    "ISL (mm)"                       FLOAT(36),
    "OSL (mm)"                       FLOAT(36),
    "Net area (mm2)"                 FLOAT(36),
    "Gross area (mm2)"               FLOAT(36),
    "FSF"                            FLOAT(36),
    "DOF"                            FLOAT(36),
    "Averaged pressure (bar)"        FLOAT(36),
    "Pressure variance"              FLOAT(36),
/*"Vertical spring rate tangent (N/mm)" FLOAT(36),*/
    "Vertical spring rate tangent (" FLOAT(36),
/*"Vertical spring rate secant (N/mm)" FLOAT(36),*/
    "Vertical spring rate secant (N" FLOAT(36),
    "Lateral spring rate (N/mm)"     FLOAT(36),
/*"Longitudinal spring rate (N/mm)" FLOAT(36),*/
    "Longitudinal spring rate (N/mm" FLOAT(36),
    "Torsional spring rate (N/mm)"   FLOAT(36),
    "RRc"                            FLOAT(36),
    "RR (kg)"                        FLOAT(36),
    "Loss (N-mm/rev)"                FLOAT(36),
    "Temperature (C)"                FLOAT(36),
    "CS (N/deg)"                     FLOAT(36),
    "SAS (N-m/deg)"                  FLOAT(36),
    "Energy (N·mm)"                  FLOAT(36),
    "Energy extrapolation (N·mm)"    FLOAT(36),
/*"Energy extrapolation (N\u00b7mm)" FLOAT(36),*/
    "Max conicity (lb)"              FLOAT(36),
    "Min conicity (lb)"              FLOAT(36),
    "Zone start ratio"               FLOAT(36),
    "Zone end ratio"                 FLOAT(36),
/*"Conicity due to belt offset (lb)" FLOAT(36),*/
    "Conicity due to belt offset (l" FLOAT(36),
    "TD"                             VARCHAR(50),
    "FP"                             VARCHAR(50),
    "SR"                             VARCHAR(50),
    "RR"                             VARCHAR(50),
    "FM"                             VARCHAR(50),
    "TP"                             VARCHAR(50),
    "COSTGV"                         VARCHAR(50),
    "COSBO"                          VARCHAR(50),
    "Zones"                          NUMBER(3),
    "Section diameter mid sidewall " FLOAT(36),
    PRIMARY KEY ("E_INDICATORS_ID"),
    CONSTRAINT "FK_B_E_TESTS_ID" FOREIGN KEY ("B_TESTS_ID") REFERENCES B_TESTS ("B_TESTS_ID") on delete cascade
);





CREATE TABLE APPENDIX_FP
(
    "APPENDIX_FP_ID"                NUMBER(36) NOT NULL,
    "E_INDICATORS_ID"               NUMBER(36),
    "Test-load-pressure-rib ID"     VARCHAR(50),
    "Test-load-pressure ID"         VARCHAR(50),
    "Zone"                          FLOAT(36),
    "Max length (mm)"               FLOAT(36),
    "Max width (mm)"                FLOAT(36),
    "Net area (mm2)"                FLOAT(36),
    "Average pressure (bar)"        FLOAT(36),
    "Length at 10% of width (mm)"   FLOAT(36),
    "Length at 20% of width (mm)"   FLOAT(36),
    "Length at 30% of width (mm)"   FLOAT(36),
    "Length at 50% of width (mm)"   FLOAT(36),
    "Length at 70% of width (mm)"   FLOAT(36),
    "Length at 80% of width (mm)"   FLOAT(36),
    "Length at 90% of width (mm)"   FLOAT(36),
    "AP ratio ISL OSL"              FLOAT(36),
    "AP ratio OSL ISL"              FLOAT(36),
    PRIMARY KEY ("APPENDIX_FP_ID"),
    CONSTRAINT "FK_E_APPENDIX_FP_ID" FOREIGN KEY ("E_INDICATORS_ID") REFERENCES E_INDICATORS ("E_INDICATORS_ID") on delete cascade
);





CREATE TABLE APPENDIX_RR
(
    "APPENDIX_RR_ID"                    NUMBER(36) NOT NULL,
    "E_INDICATORS_ID"                   NUMBER(36),
/*"Test-load-pressure-component ID"     VARCHAR(50),*/
    "Test-load-pressure-component I"    VARCHAR(50),
    "Test-load-pressure ID"             VARCHAR(50),
    "Component"                         VARCHAR(50),
    "Energy Diss. Per Rev. (N-mm)"      FLOAT(36),
    "Energy Diss. % of Total"           FLOAT(36),
    PRIMARY KEY ("APPENDIX_RR_ID"),
    CONSTRAINT "FK_E_APPENDIX_RR_ID" FOREIGN KEY ("E_INDICATORS_ID") REFERENCES E_INDICATORS ("E_INDICATORS_ID") on delete cascade
);






CREATE TABLE A_CCSD_EXTRA
(
    "A_CCSD_EXTRA_ID"               NUMBER(36) NOT NULL,
    "A_CCSD_ID"                     NUMBER(36),
    "Column name"                   VARCHAR(50),
    "Column value"                  VARCHAR(50),
    PRIMARY KEY ("A_CCSD_EXTRA_ID"),
    CONSTRAINT FK_A_CCSD_ID FOREIGN KEY ("A_CCSD_ID")
        REFERENCES A_CCSD ("A_CCSD_ID") on delete cascade
);



CREATE TABLE B_TESTS_EXTRA
(
    "B_TESTS_EXTRA_ID"              NUMBER(36) NOT NULL,
    "B_TESTS_ID"                    NUMBER(36),
    "Column name"                   VARCHAR(50),
    "Column value"                  VARCHAR(50),
    PRIMARY KEY ("B_TESTS_EXTRA_ID"),
    CONSTRAINT FK_B_TEST_ID FOREIGN KEY ("B_TESTS_ID")
        REFERENCES B_TESTS ("B_TESTS_ID") on delete cascade
);



CREATE TABLE C_COMPONENTS_EXTRA
(
    "C_COMPONENTS_EXTRA_ID"         NUMBER(36) NOT NULL,
    "C_COMPONENTS_ID"               NUMBER(36),
    "Column name"                   VARCHAR(50),
    "Column value"                  VARCHAR(50),
    PRIMARY KEY ("C_COMPONENTS_EXTRA_ID"),
    CONSTRAINT FK_C_COMPONENTS_ID FOREIGN KEY ("C_COMPONENTS_ID")
        REFERENCES C_COMPONENTS ("C_COMPONENTS_ID") on delete cascade
);



CREATE TABLE D_REINFORCEMENTS_EXTRA
(
    "D_REINFORCEMENTS_EXTRA_ID"     NUMBER(36) NOT NULL,
    "D_REINFORCEMENTS_ID"           NUMBER(36),
    "Column name"                   VARCHAR(50),
    "Column value"                  VARCHAR(50),
    PRIMARY KEY ("D_REINFORCEMENTS_EXTRA_ID"),
    CONSTRAINT FK_D_REINFORCEMENTS_ID FOREIGN KEY ("D_REINFORCEMENTS_ID")
        REFERENCES D_REINFORCEMENTS ("D_REINFORCEMENTS_ID") on delete cascade
);

CREATE TABLE E_INDICATORS_EXTRA
(
    "E_INDICATORS_EXTRA_ID"         NUMBER(36) NOT NULL,
    "E_INDICATORS_ID"               NUMBER(36),
    "Column name"                   VARCHAR(50),
    "Column value"                  VARCHAR(50),
    PRIMARY KEY ("E_INDICATORS_EXTRA_ID"),
    CONSTRAINT FK_E_INDICATORS_ID FOREIGN KEY ("E_INDICATORS_ID")
        REFERENCES E_INDICATORS ("E_INDICATORS_ID") on delete cascade
);




CREATE TABLE APPENDIX_FP_Extra
(
    "APPENDIX_FP_EXTRA_ID"              NUMBER(36) NOT NULL,
    "APPENDIX_FP_ID"                    NUMBER(36),
    "Column name"                       VARCHAR(50),
    "Column value"                      VARCHAR(50),
    PRIMARY KEY ("APPENDIX_FP_EXTRA_ID"),
    CONSTRAINT FK_Appendix_FP_ID FOREIGN KEY ("APPENDIX_FP_ID")
        REFERENCES APPENDIX_FP ("APPENDIX_FP_ID") on delete cascade
);




CREATE TABLE APPENDIX_RR_Extra
(
    "APPENDIX_RR_EXTRA_ID"              NUMBER(36) NOT NULL,
    "APPENDIX_RR_ID"                    NUMBER(36),
    "Column name"                       VARCHAR(50),
    "Column value"                      VARCHAR(50),
    PRIMARY KEY ("APPENDIX_RR_EXTRA_ID"),
    CONSTRAINT FK_Appendix_RR_ID FOREIGN KEY ("APPENDIX_RR_ID")
        REFERENCES APPENDIX_RR ("APPENDIX_RR_ID") on delete cascade
);




create sequence shared_sequence;

--drop table attached_file;
create table attached_file
( file_id number(36) not null
, parent_id number(36) not null
, file_name varchar2(250) not null
, object_name varchar2(250) not null
, cloud_upload_status varchar2(10)
, inserted_on timestamp
, updated_on timestamp
, constraint pk_attached_file primary key (file_id)
);

-- Tracking & model binding status (one-to-one relationship with A_CCSD)
--drop table a_ccsd_status;
create table a_ccsd_status
( a_ccsd_id number(36) not null
, source_file_id number(36) not null
, created_on timestamp
, created_by varchar2(50)
, binding_status varchar2(50)
, bound_on timestamp
, bound_by varchar2(50)
, binding_proc_sid number(10)
-- More columns to come here...
, constraint pk_a_ccsd_status primary key (a_ccsd_id)
, constraint fk_a_ccsd_status foreign key (a_ccsd_id) references a_ccsd (a_ccsd_id) on delete cascade
);

-- Experimental test results bound to FEA data from indicators
create table ctl
( a_ccsd_id number(36) not null
, b_tests_id number(36) not null
, e_indicators_id number(36) not null
, result_category varchar2(2) not null
, result_name varchar2(100) not null
, result_code varchar(10) not null
, test_request_number varchar2(10) not null
, tire_construction varchar2(10) not null
, tire_serial varchar2(3) not null
, fea_load_kgf number(6, 1)
, fea_inflation_bar number(5, 2)
, fea_value number not null
, exp_load_kgf number(6, 1)
, exp_inflation_bar number(5, 2)
, exp_value number not null
, value_unit varchar2(6) not null
, constraint fk_ctl foreign key (e_indicators_id) references e_indicators (e_indicators_id) on delete cascade
);



