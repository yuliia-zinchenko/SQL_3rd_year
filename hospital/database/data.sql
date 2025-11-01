--
-- PostgreSQL database dump
--

\restrict 5LeNW4Bc0HxPfSq3lQrkz7cUUJwFH1k5uK840qc18PeAwalaG0J6zeeVnnSmvCY

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: postgres
--

SET SESSION AUTHORIZATION DEFAULT;

ALTER TABLE public.departments DISABLE TRIGGER ALL;

COPY public.departments (department_id, name, description) FROM stdin;
1	Therapy	\N
\.


ALTER TABLE public.departments ENABLE TRIGGER ALL;

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.users DISABLE TRIGGER ALL;

COPY public.users (user_id, username, password_hash, staff_id) FROM stdin;
1	admin	some_hash	\N
\.


ALTER TABLE public.users ENABLE TRIGGER ALL;

--
-- Data for Name: staff; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.staff DISABLE TRIGGER ALL;

COPY public.staff (staff_id, first_name, last_name, contact_info, department_id, created_at, updated_at, updated_by) FROM stdin;
1	Gregory	House	\N	1	2025-11-01 18:15:08.608977+02	\N	1
\.


ALTER TABLE public.staff ENABLE TRIGGER ALL;

--
-- Data for Name: doctors; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.doctors DISABLE TRIGGER ALL;

COPY public.doctors (doctor_id, specialization) FROM stdin;
1	Diagnostician
\.


ALTER TABLE public.doctors ENABLE TRIGGER ALL;

--
-- Name: departments_department_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.departments_department_id_seq', 1, true);


--
-- Name: staff_staff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.staff_staff_id_seq', 1, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

\unrestrict 5LeNW4Bc0HxPfSq3lQrkz7cUUJwFH1k5uK840qc18PeAwalaG0J6zeeVnnSmvCY

