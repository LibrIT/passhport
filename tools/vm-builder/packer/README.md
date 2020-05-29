Build image with packer
=============================

You can build images with packer (https://www.packer.io/).

To build an image with qemu builder :
```
packer build passhport-qemu-iso.json
 ```

To build an image on scaleway :
```
packer build -var "git_sha=$(git rev-parse --short HEAD)" passhport-scaleway.json
 ```

(read the jsons file so that you'll know the env vars you'll need)
