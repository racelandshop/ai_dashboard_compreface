# AI Facial Recognition Dashboard


**Note on documentation about API keys** - 

Submited a github issue. Waiting for response




**NOTE** Everything bellow here should be updated/double checked

Backend for the AI Facial Recognition Dashboard for homeland

This dashboard creates an entity called ```image_processing.face_recognition_central```, which acts as the central processing unit of the whole integration. 
Its responsible for scaning, registering and predicting faces

# Deeptack docker 

Run the following command to have access to the docker command

docker run -e VISION-DETECTION=True -e VISION-FACE=True -v localstorage:/datastore -p 80:5000 deepquestai/deepstack

# Notes on the number of faces being trained: 
From their API FAQ: https://docs.deepstack.cc/faq/index.html#apis-face

### How does Face Recognition works?
The face recognition API allows you to register a name/id with a face by sending at least 1 image containing the person’s face and corresponding name/id. Once a face has been registered, you can send any other image containing the person’s face or with other faces as well to find and identify the registered person(s) by name/id.

There is no limit to the the number of faces you send for improved recognition accuracy. It is recommended that you ensure you provide diverse images of the person’s face if you are providing multiple image samples for face registration.

Visit the Face Recognition page in this documentation for the sample code.

### What if I try to recognize a face I haven’t registered?
The Face API will still return a detected a face but it will be recognized as unknown.

### Can I update a registered face with more images?
Yes. All you need to do is to send a POST request with the new image using the exact same name/id you used for the previous registration.

# Notes on automation: 

Example of scan service: 

```
service: ai_dashboard.scan
data:
  camera_scan_entity_id: camera_entity_id
target:
  entity_id: image_processing.face_recognition_central
```

After the scan the image_processing entity update its attributes. This has the information on the number of faces, if any face was recognized  and other metrics

# 


# Dev test:
I recommend using a virtual enviroment for the following

Install the test requirements ```requirements_test.txt```

In the newest version of pytest-homeassistant-custom-component (0.12.29) the test need to be marked by @pytest.mark.asyncio or the pytest command need the flag --asyncio-mode=auto

e.g. 
``` pytest tests/ --asyncio-mode=auto ```

You might need to run the pytest using the -m flag if the above command dones not work

``` python3 -m pytest tests```

