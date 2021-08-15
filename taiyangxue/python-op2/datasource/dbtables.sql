/*
 Navicat Premium Data Transfer

 Source Server         : sale3
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 12/08/2021 00:57:47
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for tbas_score
-- ----------------------------
DROP TABLE IF EXISTS "tbas_score";
CREATE TABLE "tbas_score" (
  "type" TEXT,
  "value" integer,
  "title" TEXT
);

-- ----------------------------
-- Table structure for tprj_activity
-- ----------------------------
DROP TABLE IF EXISTS "tprj_activity";
CREATE TABLE "tprj_activity" (
  "mixin_id" INTEGER NOT NULL,
  "std_id" INTEGER,
  "date" TEXT,
  "type" text,
  "count" INTEGER,
  "check_type" TEXT,
  "cal_done" real
);

-- ----------------------------
-- Table structure for tprj_leader_score
-- ----------------------------
DROP TABLE IF EXISTS "tprj_leader_score";
CREATE TABLE "tprj_leader_score" (
  "mixin_id" INTEGER,
  "score" integer
);

-- ----------------------------
-- Table structure for tprj_team_check_rate
-- ----------------------------
DROP TABLE IF EXISTS "tprj_team_check_rate";
CREATE TABLE "tprj_team_check_rate" (
  "team" TEXT,
  "date" TEXT,
  "rate" integer
);

-- ----------------------------
-- Table structure for tprj_team_score
-- ----------------------------
DROP TABLE IF EXISTS "tprj_team_score";
CREATE TABLE "tprj_team_score" (
  "team" TEXT,
  "score" integer
);

-- ----------------------------
-- Table structure for tprj_team_score_detail
-- ----------------------------
DROP TABLE IF EXISTS "tprj_team_score_detail";
CREATE TABLE "tprj_team_score_detail" (
  "team" TEXT,
  "score" integer,
  "date" TEXT
);

-- ----------------------------
-- Table structure for tprj_user
-- ----------------------------
DROP TABLE IF EXISTS "tprj_user";
CREATE TABLE "tprj_user" (
  "mixin_id" INTEGER NOT NULL,
  "std_id" INTEGER,
  "name" TEXT,
  "team" TEXT,
  "title" TEXT,
  PRIMARY KEY ("mixin_id")
);

-- ----------------------------
-- Table structure for tprj_user_score
-- ----------------------------
DROP TABLE IF EXISTS "tprj_user_score";
CREATE TABLE "tprj_user_score" (
  "mixin_id" INTEGER,
  "score" integer,
  "team" TEXT,
  "title" TEXT
);

-- ----------------------------
-- Table structure for tprj_user_score_detail
-- ----------------------------
DROP TABLE IF EXISTS "tprj_user_score_detail";
CREATE TABLE "tprj_user_score_detail" (
  "mixin_id" INTEGER,
  "score" integer,
  "team" TEXT,
  "title" TEXT,
  "date" TEXT
);

PRAGMA foreign_keys = true;
