resource "aws_kms_key" "app" {
  description             = "KMS key for ${local.name_prefix} data encryption"
  deletion_window_in_days = 7
  enable_key_rotation     = true
  tags                    = local.common_tags
}

resource "aws_kms_alias" "app" {
  name          = "alias/${local.name_prefix}"
  target_key_id = aws_kms_key.app.key_id
}
