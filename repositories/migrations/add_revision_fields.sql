BEGIN;
ALTER TABLE "projectmgr_sourcerepository" ADD COLUMN "current_rev" varchar(50) NOT NULL DEFAULT '';
ALTER TABLE "projectmgr_sourcerepository" ADD COLUMN "previous_rev" varchar(50) NOT NULL DEFAULT '';
COMMIT;
BEGIN;
ALTER TABLE "repoman_sourcerepository" ADD COLUMN "current_rev" varchar(50) NOT NULL DEFAULT '';
ALTER TABLE "repoman_sourcerepository" ADD COLUMN "previous_rev" varchar(50) NOT NULL DEFAULT '';
COMMIT;