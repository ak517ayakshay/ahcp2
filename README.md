# Clinical Note Endpoints

## POST /apc/clinical_note/create

**Query params:** `member_id`, `composition_type: "RPM" | "CCM"`, `service_month: "May 2026"`  
**Auth:** practitioner JWT  
**Logic:** fetch member_name internally, check `fhir_compositions` → if exists return cached, else invoke medulla workflow → validate → persist → return note

---

## GET /apc/clinical_note/read

**Query params:** `member_id`, `composition_type`, `service_month`  
**Auth:** practitioner JWT  
**Logic:** read from `fhir_compositions`, 404 if not found

---

## PUT /apc/clinical_note/update

**Query params:** `member_id`, `composition_type`, `service_month`  
**Auth:** practitioner JWT  
**Logic:** (even if exists) → overwrite in `fhir_compositions`

---

## DELETE /apc/clinical_note/delete

**Query params:** `member_id`, `composition_type`, `service_month`  
**Auth:** practitioner JWT

---

# Monthly Report Endpoints

## POST /apc/monthly_report/create

**Query params:** `provider_id`, `composition_type: "RPM" | "CCM"`, `service_month: "May 2026"`  
**Auth:** practitioner JWT  
**Logic:** find all qualifying members → aggregate → generate billing summary → persist

---

## GET /apc/monthly_report/read

**Query params:** `provider_id`, `composition_type`, `service_month`  
**Auth:** practitioner JWT

---

## PUT /apc/monthly_report/update

**Query params:** `provider_id`, `composition_type`, `service_month`  
**Auth:** practitioner JWT  
**Logic:** overwrite
