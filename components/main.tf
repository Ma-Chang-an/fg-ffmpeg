terraform {
  required_providers {
    huaweicloud = {
      source  = "huawei.com/provider/huaweicloud"
      version = ">= 1.59.1"
    }
  }
}

# Configure the HuaweiCloud Provider
provider "huaweicloud" {
  endpoints = {
    apig = var.region == "cn-north-7" ? format("apig.%s.ulanqab.huawei.com", var.region) : format("apig.%s.myhuaweicloud.com", var.region)
    obs  = var.region == "cn-north-7" ? format("obs.%s.ulanqab.huawei.com", var.region) : format("obs.%s.myhuaweicloud.com", var.region)
    fgs  = var.region == "cn-north-7" ? format("functiongraph.%s.ulanqab.huawei.com", var.region) : format("functiongraph.%s.myhuaweicloud.com", var.region)
  }
  auth_url = format("https://iam.%s.myhuaweicloud.com/v3", var.region)
  insecure = true
  region   = var.region
}
locals {
  timestamp = formatdate("YYYYMMDDhhmmss", timestamp())
  obs       = var.region == "cn-north-7" ? format("obs.%s.ulanqab.huawei.com", var.region) : format("obs.%s.myhuaweicloud.com", var.region)
}

resource "huaweicloud_identity_agency" "agency" {
  count                  = var.agency_name == "" ? 1 : 0
  name                   = "fgs-app-adminagency"
  description            = "agency"
  delegated_service_name = "op_svc_cff"

  all_resources_roles = ["OBS Administrator", "DIS Administrator", "LTS Administrator", "NLP Administrator", "MPC Administrator", "VPC Administrator", "SWR FullAccess", "SFS Turbo FullAccess", "SFS FullAccess"]
}

resource "huaweicloud_fgs_function" "ffmpeg-audio-convert" {
  name                  = format("%s_%s", "ffmpeg-audio-convert", local.timestamp)
  functiongraph_version = "v2"
  agency                = var.agency_name != "" ? var.agency_name : huaweicloud_identity_agency.agency[0].name
  handler               = "-"
  app                   = "default"
  runtime               = "Custom"
  memory_size           = 512
  timeout               = 600
  user_data             = format("{\"ENDPOINT\":\"%s\"}", local.obs)
  custom_image {
    url = format("swr.%s.myhuaweicloud.com/custom_container/fg-ffmpeg:audio-convert-%s", var.region, var.image_version)
  }
}

resource "huaweicloud_fgs_function" "ffmpeg-get-duration" {
  name                  = format("%s_%s", "ffmpeg-get-duration", local.timestamp)
  functiongraph_version = "v2"
  agency                = var.agency_name != "" ? var.agency_name : huaweicloud_identity_agency.agency[0].name
  handler               = "-"
  app                   = "default"
  runtime               = "Custom"
  memory_size           = 512
  timeout               = 600
  user_data             = format("{\"ENDPOINT\":\"%s\"}", local.obs)
  custom_image {
    url = format("swr.%s.myhuaweicloud.com/custom_container/fg-ffmpeg:get-duration-%s", var.region, var.image_version)
  }
}

resource "huaweicloud_fgs_function" "ffmpeg-get-meta" {
  name                  = format("%s_%s", "ffmpeg-get-meta", local.timestamp)
  functiongraph_version = "v2"
  agency                = var.agency_name != "" ? var.agency_name : huaweicloud_identity_agency.agency[0].name
  handler               = "-"
  app                   = "default"
  runtime               = "Custom"
  memory_size           = 512
  timeout               = 600
  user_data             = format("{\"ENDPOINT\":\"%s\"}", local.obs)
  custom_image {
    url = format("swr.%s.myhuaweicloud.com/custom_container/fg-ffmpeg:get-meta-%s", var.region, var.image_version)
  }
}

resource "huaweicloud_fgs_function" "ffmpeg-get-sprites" {
  name                  = format("%s_%s", "ffmpeg-get-sprites", local.timestamp)
  functiongraph_version = "v2"
  agency                = var.agency_name != "" ? var.agency_name : huaweicloud_identity_agency.agency[0].name
  handler               = "-"
  app                   = "default"
  runtime               = "Custom"
  memory_size           = 512
  timeout               = 600
  user_data             = format("{\"ENDPOINT\":\"%s\"}", local.obs)
  custom_image {
    url = format("swr.%s.myhuaweicloud.com/custom_container/fg-ffmpeg:get-sprites-%s", var.region, var.image_version)
  }
}

resource "huaweicloud_fgs_function" "ffmpeg-video-gif" {
  name                  = format("%s_%s", "ffmpeg-video-gif", local.timestamp)
  functiongraph_version = "v2"
  agency                = var.agency_name != "" ? var.agency_name : huaweicloud_identity_agency.agency[0].name
  handler               = "-"
  app                   = "default"
  runtime               = "Custom"
  memory_size           = 512
  timeout               = 600
  user_data             = format("{\"ENDPOINT\":\"%s\"}", local.obs)
  custom_image {
    url = format("swr.%s.myhuaweicloud.com/custom_container/fg-ffmpeg:video-gif-%s", var.region, var.image_version)
  }
}

resource "huaweicloud_fgs_function" "ffmpeg-video-watermark" {
  name                  = format("%s_%s", "ffmpeg-video-watermark", local.timestamp)
  functiongraph_version = "v2"
  agency                = var.agency_name != "" ? var.agency_name : huaweicloud_identity_agency.agency[0].name
  handler               = "-"
  app                   = "default"
  runtime               = "Custom"
  memory_size           = 512
  timeout               = 600
  user_data             = format("{\"ENDPOINT\":\"%s\"}", local.obs)
  custom_image {
    url = format("swr.%s.myhuaweicloud.com/custom_container/fg-ffmpeg:video-watermark-%s", var.region, var.image_version)
  }
}

resource "huaweicloud_fgs_async_invoke_configuration" "ffmpeg-audio-convert" {
  function_urn                   = huaweicloud_fgs_function.ffmpeg-audio-convert.id
  max_async_event_age_in_seconds = 3600
  max_async_retry_attempts       = 3
  enable_async_status_log        = true
}

resource "huaweicloud_fgs_async_invoke_configuration" "ffmpeg-get-sprites" {
  function_urn                   = huaweicloud_fgs_function.ffmpeg-get-sprites.id
  max_async_event_age_in_seconds = 3600
  max_async_retry_attempts       = 3
  enable_async_status_log        = true
}

resource "huaweicloud_fgs_async_invoke_configuration" "ffmpeg-video-gif" {
  function_urn                   = huaweicloud_fgs_function.ffmpeg-video-gif.id
  max_async_event_age_in_seconds = 3600
  max_async_retry_attempts       = 3
  enable_async_status_log        = true
}

resource "huaweicloud_fgs_async_invoke_configuration" "ffmpeg-video-watermark" {
  function_urn                   = huaweicloud_fgs_function.ffmpeg-video-watermark.id
  max_async_event_age_in_seconds = 3600
  max_async_retry_attempts       = 3
  enable_async_status_log        = true
}