--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4
-- Dumped by pg_dump version 12.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: valerian
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO valerian;

--
-- Name: customers; Type: TABLE; Schema: public; Owner: valerian
--

CREATE TABLE public.customers (
    id integer NOT NULL,
    name character varying(200),
    city character varying,
    adress character varying(150),
    phone character varying(30),
    social_media character varying(100),
    image_link character varying(500)
);


ALTER TABLE public.customers OWNER TO valerian;

--
-- Name: customers_id_seq; Type: SEQUENCE; Schema: public; Owner: valerian
--

CREATE SEQUENCE public.customers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customers_id_seq OWNER TO valerian;

--
-- Name: customers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: valerian
--

ALTER SEQUENCE public.customers_id_seq OWNED BY public.customers.id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: valerian
--

CREATE TABLE public.events (
    id integer NOT NULL,
    event_name character varying,
    event_type character varying,
    date timestamp without time zone,
    rating integer,
    customer_id integer,
    provider_id integer
);


ALTER TABLE public.events OWNER TO valerian;

--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: valerian
--

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_id_seq OWNER TO valerian;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: valerian
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: providers; Type: TABLE; Schema: public; Owner: valerian
--

CREATE TABLE public.providers (
    id integer NOT NULL,
    name character varying(200),
    services_offered character varying(200),
    city character varying,
    adress character varying(150),
    phone character varying(30),
    website character varying(120),
    social_media character varying(500),
    image_link character varying(700)
);


ALTER TABLE public.providers OWNER TO valerian;

--
-- Name: providers_id_seq; Type: SEQUENCE; Schema: public; Owner: valerian
--

CREATE SEQUENCE public.providers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.providers_id_seq OWNER TO valerian;

--
-- Name: providers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: valerian
--

ALTER SEQUENCE public.providers_id_seq OWNED BY public.providers.id;


--
-- Name: customers id; Type: DEFAULT; Schema: public; Owner: valerian
--

ALTER TABLE ONLY public.customers ALTER COLUMN id SET DEFAULT nextval('public.customers_id_seq'::regclass);


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: valerian
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Name: providers id; Type: DEFAULT; Schema: public; Owner: valerian
--

ALTER TABLE ONLY public.providers ALTER COLUMN id SET DEFAULT nextval('public.providers_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: valerian
--

COPY public.alembic_version (version_num) FROM stdin;
06446fea8dbe
\.


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: valerian
--

COPY public.customers (id, name, city, adress, phone, social_media, image_link) FROM stdin;
1	Test	TESTING CITY	test adress	testphone	test social	image
2	Test	TESTING CITY	test adress	testphone	test social	image
5	Test	TESTING CITY	test adress	testphone	test social	image
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: valerian
--

COPY public.events (id, event_name, event_type, date, rating, customer_id, provider_id) FROM stdin;
1	photoshoot	foto	2020-03-04 00:00:00	\N	\N	\N
2	photoshoot	foto	2020-03-04 00:00:00	\N	\N	\N
5	photoshoot	foto	2020-03-04 00:00:00	\N	\N	\N
\.


--
-- Data for Name: providers; Type: TABLE DATA; Schema: public; Owner: valerian
--

COPY public.providers (id, name, services_offered, city, adress, phone, website, social_media, image_link) FROM stdin;
1	Test	TEST	TESTING CITY	test adress	testphone	test website	test social	image
2	Test	TEST	TESTING CITY	test adress	testphone	test website	test social	image
5	Test	TEST	TESTING CITY	test adress	testphone	test website	test social	image
6	NAME	\N	CITY	ADDRESS	PHONE	\N	facemol	immage
\.


--
-- Name: customers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: valerian
--

SELECT pg_catalog.setval('public.customers_id_seq', 5, true);


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: valerian
--

SELECT pg_catalog.setval('public.events_id_seq', 5, true);


--
-- Name: providers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: valerian
--

SELECT pg_catalog.setval('public.providers_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: valerian
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: valerian
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: valerian
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: providers providers_pkey; Type: CONSTRAINT; Schema: public; Owner: valerian
--

ALTER TABLE ONLY public.providers
    ADD CONSTRAINT providers_pkey PRIMARY KEY (id);


--
-- Name: events events_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: valerian
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: events events_provider_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: valerian
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES public.providers(id);


--
-- PostgreSQL database dump complete
--

