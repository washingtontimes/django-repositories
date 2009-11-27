BEGIN;
ALTER TABLE "projectmgr_sourcerepository" DROP COLUMN "current_rev";
ALTER TABLE "projectmgr_sourcerepository" DROP COLUMN "previous_rev";
COMMIT;