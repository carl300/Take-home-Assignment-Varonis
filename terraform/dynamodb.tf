resource "aws_dynamodb_table" "restaurants" {
  name         = "${local.name_prefix}-restaurants"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.app.arn
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = local.common_tags
}

resource "aws_dynamodb_table" "request_logs" {
  name         = "${local.name_prefix}-request-logs"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "requestId"

  attribute {
    name = "requestId"
    type = "S"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.app.arn
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = local.common_tags
}

locals {
  seed_restaurants = {
    "queen-city-pizza" = {
      name       = "Queen City Pizza"
      style      = "Italian"
      address    = "101 South End Blvd, Charlotte, NC"
      openHour   = "09:00"
      closeHour  = "23:00"
      vegetarian = true
      delivery   = true
    }


    "south-end-pasta" = {
      name       = "South End Pasta House"
      style      = "Italian"
      address    = "212 Camden Rd, Charlotte, NC"
      openHour   = "11:00"
      closeHour  = "22:00"
      vegetarian = false
      delivery   = true
    }

    "uptown-bistro" = {
      name       = "Uptown Bistro"
      style      = "French"
      address    = "300 Trade Street, Charlotte, NC"
      openHour   = "10:00"
      closeHour  = "21:00"
      vegetarian = true
      delivery   = false
    }

    "charlotte-brasserie" = {
      name       = "Charlotte Brasserie"
      style      = "French"
      address    = "88 Tryon Street, Charlotte, NC"
      openHour   = "11:00"
      closeHour  = "22:00"
      vegetarian = false
      delivery   = true
    }

    "seoul-garden" = {
      name       = "Seoul Garden"
      style      = "Korean"
      address    = "120 Matthews Station St, Matthews, NC"
      openHour   = "10:00"
      closeHour  = "22:00"
      vegetarian = true
      delivery   = true
    }

    "kimchi-kitchen" = {
      name       = "Kimchi Kitchen"
      style      = "Korean"
      address    = "55 Independence Blvd, Charlotte, NC"
      openHour   = "10:00"
      closeHour  = "23:00"
      vegetarian = false
      delivery   = true
    }

    "lake-norman-grill" = {
      name       = "Lake Norman Grill"
      style      = "American"
      address    = "500 Lake Norman Dr, Huntersville, NC"
      openHour   = "08:00"
      closeHour  = "22:00"
      vegetarian = false
      delivery   = true
    }

    "green-fork-cafe" = {
      name       = "Green Fork Cafe"
      style      = "Vegetarian"
      address    = "18 Park Road, Charlotte, NC"
      openHour   = "08:00"
      closeHour  = "20:00"
      vegetarian = true
      delivery   = false
    }

    "night-tacos" = {
      name       = "Night Tacos"
      style      = "Mexican"
      address    = "77 Central Ave, Charlotte, NC"
      openHour   = "18:00"
      closeHour  = "02:00"
      vegetarian = true
      delivery   = true
    }

    "open-kitchen" = {
      name       = "Open Kitchen"
      style      = "Italian"
      address    = "100 Freedom Drive, Charlotte, NC"
      openHour   = "00:00"
      closeHour  = "23:59"
      vegetarian = true
      delivery   = true
    }

  }
}

resource "aws_dynamodb_table_item" "restaurants" {
  for_each   = local.seed_restaurants
  table_name = aws_dynamodb_table.restaurants.name
  hash_key   = aws_dynamodb_table.restaurants.hash_key

  item = jsonencode({
    id          = { S = each.key }
    name        = { S = each.value.name }
    style       = { S = each.value.style }
    style_lower = { S = lower(each.value.style) }
    address     = { S = each.value.address }
    openHour    = { S = each.value.openHour }
    closeHour   = { S = each.value.closeHour }
    vegetarian  = { BOOL = each.value.vegetarian }
    delivery    = { BOOL = each.value.delivery }
  })
}
