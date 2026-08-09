# Plan Técnico de Hardening e Integración — Rama `feature/alan-hu08`
**Programador:** Alan Geovani Arriaga Quintana (Programador 1 — Backend Core & DB)

## Contexto y Delimitación del Entregable

> [!NOTE]
> La Historia de Usuario **HU06 (Backend Core & DB)** fue formalmente cerrada, auditada y subida en `feature/alan-hu06`.
> Las tareas descritas en este plan pertenecen a **`feature/alan-hu08`** y corresponden a **Hardening, Aislamiento Multi-Tenant, Pruebas de Infraestructura e Integración Transversal**. No representan una reapertura de HU06.

> [!CAUTION]
> **RESTRICCIÓN DE CONTROL DE CAMBIOS:** Queda estrictamente prohibido ejecutar `git push`. Todos los entregables, migraciones y scripts de prueba se ejecutarán y conservarán exclusivamente en el entorno local de la rama `feature/alan-hu08`.

---

## Directivas y Validaciones de Auditoría Previa

### 1. Extensión de Estados de Mesa (`WAITING_BILL` y `pendingTableStatus`)
- **Validación previa:** Confirmar que no exista duplicación con la máquina de estados existente en `restaurant-floor.application-service.js`. Centralizar las transiciones permitidas (`OCCUPIED` → `WAITING_BILL` → `DIRTY` → `AVAILABLE`).
- **Resguardo DB:** Incorporar `WAITING_BILL` al enum `TableStatus` y `pendingTableStatus` a `TableSession` para conservar la transición pendiente cuando exista una operación externa (ej. cobro diferido) que requiera confirmación antes de liberar el recurso.
- **Sin Endpoints innecesarios:** Se utilizará la estructura existente sin crear endpoints ajenos al alcance Core DB.

### 2. Frontera e Integración con HU04 (POS)
- **Cero Modificación Directa:** **NO** se modificará `pos.application-service.js`, ni flujos de pago, confirmaciones CARD o checkout POS.
- **Entregable Core:** Documentar el contrato de integración (`INTEGRATION_SPEC_HU04_HU06.md`) explicitando el hook que debe invocar el módulo POS al finalizar la transacción CARD (`COMPLETED`).

### 3. Frontera e Integración con HU03 (Inventario)
- **Auditoría Previa Obligatoria:** Antes de alterar `kitchen.repository.js`, auditar si `inventoryRepository.adjustReservation` soporta un parámetro transaccional (`tx`).
- **Estrategia Condicional:**
  - *Si soporta `tx`:* Encapsular la reservación dentro de `prisma.$transaction`.
  - *Si no soporta `tx`:* **NO** realizar refactorización invasiva sobre HU03. Documentar el requerimiento de extensión en la interfaz del módulo Inventario.

### 4. Feature Flag RESTAURANT & Seguridad Tenant Auth
- **Compatibilidad con Tenant Auth:** El middleware `requireTenantModule('RESTAURANT')` reutilizará la arquitectura existente (`req.tenant`), consultando la relación `TenantModule` sin duplicar permisos RBAC.
- **Exposición en Auth:** Retornar los módulos contratados en `login` y `/me` para consumo de Frontend.

### 5. Pruebas de Infraestructura HU08
- Enfoque exclusivo en infraestructura y backend: aislamiento por tenant, aislamiento por branch, restricciones de llaves foráneas (FK), transiciones de estados inválidas, bloqueo por módulo no contratado y manejo de stock insuficiente.
- Sin dependencias de UI o flujos de interfaz de usuario.

---

## Matriz de Pre-Implementación (Archivos, Justificación y Riesgos)

Antes de modificar el código fuente, se establece la siguiente matriz de cambios:

| Archivo a Modificar / Crear | Justificación del Cambio | Riesgo Asociado | Confirmación Afectación HU06 |
|---|---|---|---|
| [schema.prisma](file:///c:/Users/alanq/OneDrive/Documentos/trabajo/recidencia/impulsasuite/impulsasuiteback/prisma/schema.prisma) | Extender enum `TableStatus` (`WAITING_BILL`) y `TableSession` (`pendingTableStatus`). | Bajo. Requiere `npx prisma db push` o `npx prisma validate`. | **Sin afectación a HU06.** Campo nullable y valor enum no destructivos. |
| [restaurant-floor.application-service.js](file:///c:/Users/alanq/OneDrive/Documentos/trabajo/recidencia/impulsasuite/impulsasuiteback/src/modules/restaurant-floor/application/services/restaurant-floor.application-service.js) | Centralizar máquina de estados y validar transiciones (`OCCUPIED` → `WAITING_BILL` → `DIRTY` → `AVAILABLE`). | Bajo. Retorna `409 Conflict` en transiciones inválidas. | **Sin afectación a HU06.** Refuerza la lógica sin alterar firmas de métodos existentes. |
| [tenant-module.middleware.js](file:///c:/Users/alanq/OneDrive/Documentos/trabajo/recidencia/impulsasuite/impulsasuiteback/src/modules/tenant-auth/middlewares/tenant-module.middleware.js) *(NUEVO)* | Crear middleware `requireTenantModule` para validar módulos contratados por tenant. | Bajo. Componente aislado en `tenant-auth`. | **Sin afectación a HU06.** Componente nuevo de infraestructura. |
| [restaurant-floor.routes.js](file:///c:/Users/alanq/OneDrive/Documentos/trabajo/recidencia/impulsasuite/impulsasuiteback/src/modules/restaurant-floor/routes/restaurant-floor.routes.js) | Proteger grupo de rutas con `requireTenantModule('RESTAURANT')`. | Bajo. Retorna `403` si el tenant no tiene contratado el módulo. | **Sin afectación a HU06.** Capa de ruteo/seguridad. |
| [kitchen.routes.js](file:///c:/Users/alanq/OneDrive/Documentos/trabajo/recidencia/impulsasuite/impulsasuiteback/src/modules/kitchen/routes/kitchen.routes.js) | Proteger grupo de rutas con `requireTenantModule('RESTAURANT')`. | Bajo. Retorna `403` si el tenant no tiene contratado el módulo. | **Sin afectación a HU06.** Capa de ruteo/seguridad. |
| [tenant-auth.application-service.js](file:///c:/Users/alanq/OneDrive/Documentos/trabajo/recidencia/impulsasuite/impulsasuiteback/src/modules/tenant-auth/application/services/tenant-auth.application-service.js) | Incluir array `modules` en respuestas de `login` y `/me`. | Muy Bajo. Agrega propiedad informativa a la respuesta. | **Sin afectación a HU06.** Compatibilidad garantizada. |
| [kitchen.repository.js](file:///c:/Users/alanq/OneDrive/Documentos/trabajo/recidencia/impulsasuite/impulsasuiteback/src/modules/kitchen/infrastructure/repositories/kitchen.repository.js) | Pre-validar `availableStock` antes de crear comanda. (Ajuste a transacción sujeto a auditoría de `inventoryRepository`). | Medio. Condicionado a la auditoría previa de HU03. | **Sin afectación a HU06.** Preserva contrato de comandas. |
| [INTEGRATION_SPEC_HU04_HU06.md](file:///c:/Users/alanq/OneDrive/Documentos/trabajo/recidencia/impulsasuite/impulsasuiteback/documentation/INTEGRATION_SPEC_HU04_HU06.md) *(NUEVO)* | Documentar contrato de integración y propuesta de hook para HU04 POS. | Nulo (Documentación). | **Sin afectación a HU06.** |
| [validate-hu08-core-limits.js](file:///c:/Users/alanq/OneDrive/Documentos/trabajo/recidencia/impulsasuite/impulsasuiteback/scripts/validate-hu08-core-limits.js) *(NUEVO)* | Script de pruebas de infraestructura de aislamiento y casos límite (HU08). | Nulo (Script de validación). | **Sin afectación a HU06.** Script de pruebas aislado. |

---

## Flujo de Ejecución y Verificación

### Fase 1: Auditoría Previa de Código
1. Verificar firma e implementación de `inventoryRepository.adjustReservation` para determinar soporte transaccional (`tx`).
2. Inspeccionar `restaurant-floor.application-service.js` para asegurar centralización de la máquina de estados.

### Fase 2: Implementación
1. Actualización de `schema.prisma`.
2. Creación del middleware `requireTenantModule`.
3. Aplicación de protección en rutas de restaurante y cocina.
4. Exposición de `modules` en `tenant-auth.application-service.js`.
5. Ajuste en `kitchen.repository.js` según resultado de auditoría.
6. Redacción de `INTEGRATION_SPEC_HU04_HU06.md`.

### Fase 3: Verificación Técnica
1. Validar esquema Prisma localmente:
   `npx prisma validate`
2. Aplicar cambios a la BD de desarrollo local:
   `npx prisma db push`
3. Ejecutar suite de pruebas de aislamiento e infraestructura local:
   `node scripts/validate-hu08-core-limits.js`
   `node scripts/validate-hu08-data-isolation.js`
4. Entregar resumen final de cambios validados.
