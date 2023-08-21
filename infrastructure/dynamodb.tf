
resource "aws_dynamodb_table" "address" {
  name             = "address"
  billing_mode     = "PAY_PER_REQUEST"
  hash_key         = "street_name"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"
  server_side_encryption {
    enabled = true
  }

  attribute {
    name = "street_name"
    type = "S"
  }

  #point_in_time_recovery {
  #  enabled = true
  #}

}