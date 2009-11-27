BEGIN;
ALTER TABLE "projectmgr_sourcerepository" RENAME TO "repoman_sourcerepository";
ALTER TABLE "projectmgr_remotesourcerepository" RENAME TO "repoman_remotesourcerepository";
ALTER TABLE "projectmgr_metadata" RENAME TO "repoman_metadata";
ALTER TABLE "projectmgr_repositorygroup" RENAME TO "repoman_repositorygroup";
ALTER TABLE "projectmgr_repositoryuser" RENAME TO "repoman_repositoryuser";

DROP INDEX "projectmgr_sourcerepository_name";
DROP INDEX "projectmgr_remotesourcerepository_repo_id";
DROP INDEX "projectmgr_remotesourcerepository_name";
DROP INDEX "projectmgr_metadata_source_repository_id";
DROP INDEX "projectmgr_repositorygroup_source_repository_id";
DROP INDEX "projectmgr_repositorygroup_group_id";
DROP INDEX "projectmgr_repositoryuser_source_repository_id";
DROP INDEX "projectmgr_repositoryuser_user_id";

CREATE INDEX "repoman_sourcerepository_name" ON "repoman_sourcerepository" ("name");
CREATE INDEX "repoman_remotesourcerepository_repo_id" ON "repoman_remotesourcerepository" ("repo_id");
CREATE INDEX "repoman_remotesourcerepository_name" ON "repoman_remotesourcerepository" ("name");
CREATE INDEX "repoman_metadata_source_repository_id" ON "repoman_metadata" ("source_repository_id");
CREATE INDEX "repoman_repositorygroup_source_repository_id" ON "repoman_repositorygroup" ("source_repository_id");
CREATE INDEX "repoman_repositorygroup_group_id" ON "repoman_repositorygroup" ("group_id");
CREATE INDEX "repoman_repositoryuser_source_repository_id" ON "repoman_repositoryuser" ("source_repository_id");
CREATE INDEX "repoman_repositoryuser_user_id" ON "repoman_repositoryuser" ("user_id");
COMMIT;
