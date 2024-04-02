variable "enterprise_project_id" {
    type        = string
    description = " Specifies enterprise_project_id"
    default     = "0"
}
variable "agency_name" {
    type        = string
    description = " Specifies the agency to which the function belongs."
    default     = ""
}
variable "region" {
    type        = string
    description = " Specifies the region."
    default     = "cn-north-7"
}
variable "image_version" {
    type        = string
    description = " Specifies the image version."
    default     = "v1"
}
variable "code_url" {
  type        = string
  description = "code_url"
}