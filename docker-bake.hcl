variable "TOR_VERSION" {
  # renovate: datasource=repology depName=alpine_3_23/tor versioning=loose
  default = "0.4.8.21-r0"
}

group "default" {
  targets = ["default"]
}

target "default" {
  platforms = ["linux/amd64", "linux/arm64"]
  tags = ["quay.io/seiferma/tor:${TOR_VERSION}", "quay.io/seiferma/tor:latest"]
  args = {
    TOR_VERSION = "${TOR_VERSION}"
  }
}

group "test" {
  targets = ["test"]
}

target "test" {
  inherits = ["default"]
  platforms = ["linux/amd64"]
  tags = ["test-image"]
}