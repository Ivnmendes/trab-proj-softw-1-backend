# **Trab Final Projeto de Software**

## **Links úteis**

- [Farmácia Digital](https://farmaciadigital.rs.gov.br/)
- [Lista de Medicamentos](https://admin.saude.rs.gov.br/upload/arquivos/202508/22100532-lista-de-medicamentos-e-formulas-nutricionais-na-farmacia-digital-rs-2025-08-22.pdf)
- [FAMURS](https://famurs.com.br/remume#inicioRemume)

## **Módulos**

## **Medications**

Principal módulo do programa, onde serão cadastrados os medicamentos, cids e documentos.

### **Modelos**

- ### **Medication**

  #### **Atributos**

  - `name`: string
  - `description`: string
  - `generic_name`: string
  - `concentration`: string
  - `components`: string
  - `cids`: m2m com CID
  - `documents`: m2m com Documento
  - `pharmacies`: m2m com Farmácia
  - `created_at`: datetime
  - `updated_at`: datetime

- ### **CID**

  #### **Atributos**

  - `name`: string
  - `description`: string
  - `code`: string
    - Deve ter um index único
  - `documents`: m2m com Documento
  - `created_at`: datetime
  - `updated_at`: datetime

- ### **Document**

  #### **Atributos**

  - `name`: string
  - `description`: string
  - `type`: choices("IDENTIFICATION", "REQUEST_FORM", "PRESCRIPTION", "CLINICAL_REPORT", "LAB_RESULTS)
  - `created_at`: datetime
  - `updated_at`: datetime

## **Map**

Módulo do programa responsável por gerenciar dados que o front vai utilizar para exibir os mapas.

### **Modelos**

- ### **Land Mark**

  #### **Atributos**

  - `name`: string
  - `description`: string
  - `latitude`: decimal
  - `longitude`: decimal
  - `image`: image
  - `created_at`: datetime
  - `updated_at`: datetime

- ### **Pharmacy**

  #### **Atributos**

  - `name`: string
  - `description`: string
  - `type`: choices("BASIC", "SPECIALIZED", "POPULAR")
    - Basic: Farmácia municipal ou rural
    - Specialized: Farmácia Estadual
    - Popular: Farmácia Popular
  - `address`: string
  - `landmark`: fk com Ponto de Referência
  - `created_at`: datetime
  - `updated_at`: datetime
