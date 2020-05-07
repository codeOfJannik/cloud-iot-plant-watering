# Notes

## Questions
- [ ] CICD: Gitlab or Cloud (Jenkins)?
- [ ] Sensor query: by Cloud request or Controler loop?
> To run all major logic in the cloud seems to be the better approach. A short example why:
> We got multiple controllers with a lot of sensors. Each controller runs its 
> own loop to query sensor data and sends it to the cloud.
