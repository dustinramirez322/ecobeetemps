The goal of this program is to help those interested in pulling basic information from their ecobee smart thermostat.  The examples given here assist in pulling local temperature information as well as temperature information from ecobee sensors.

There are several steps that must be taken within the ecobee website in order for this project to work:

1.  Sign up for a developer account at:  https://www.ecobee.com/home/developer/loginDeveloper.jsp
Once this step is complete the Developer and My Apps tab will show when you login to your ecobee account at https://www.ecobee.com: 

![image](https://user-images.githubusercontent.com/56071884/136790993-b6506a14-aa9f-436c-8dd6-22c8f73f957c.png)

2.  Select the developer option and create a new application within your console:

![image](https://user-images.githubusercontent.com/56071884/136794194-56bdc9b3-d905-4b36-95db-8adb7b214b97.png)
!Note! Set Authorization method to ecobee PIN to use this guide

  
3.  Replace 'fakeApiKey123abc' with the API key displayed in the apiKey.txt file

4.  Run the authorize script.  You should receive an output that includes your pin and code.

5.  Select "My Apps" from the side menu:

![image](https://user-images.githubusercontent.com/56071884/136806097-017a4a02-7c9e-4660-9511-825a10113eec.png)

6.  Select the "Add Application" option, input the 'ecobeePin' provided by the authorize script, and select "Validate":

![image](https://user-images.githubusercontent.com/56071884/136806524-55c215b7-682a-440c-b9f4-d607621cc048.png)

7.  Confirm your device:

![image](https://user-images.githubusercontent.com/56071884/136809699-97166619-a3dc-4ab7-88cf-5ee87ef087d9.png)  ![image](https://user-images.githubusercontent.com/56071884/136809757-cb646f18-7d4c-4fa7-a429-d97333af369f.png)
  
8.  Immediately run the access_token script.  You will receive an access and refresh token which will be written to their respective text files.
  
9.  Begin pulling data...try the get_temps to see local temperature and two sensors information.

Here's an example graph I created with this data:

![image](https://user-images.githubusercontent.com/56071884/136810690-9a444374-e691-485a-8e6d-dea7611b4c4d.png)

