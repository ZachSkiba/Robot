# 497 Project Documentation

## Week 1: Project Planning and Proposal Updates
I began by updating the project proposal and planning documents to better reflect the direction of the project and ensure that the work was aligned with the goals of the course. This involved reviewing the current project structure, adjusting the project scope, and improving the written planning materials so they were clearer and more professional.

I also met with the professor to discuss the updated proposal and plans. This was an important step in confirming that the project was moving in a satisfactory direction and that the work being completed matched the expectations for the class. These meetings allowed me to communicate the intended progress, receive feedback, and make necessary changes to ensure the project remained on track.

## Week 2: Docker Workflow Improvements
After the proposal work, I focused on fixing and improving the Docker setup so that the project could be opened and used more smoothly by all users. The goal was to make the environment more reliable and easier to work in, especially for people who were setting up the project for the first time.

This involved identifying issues in the Docker configuration, making changes to improve the workflow, and ensuring that the environment would function more consistently. A portion of this work was aimed at reducing setup problems and making the process much easier for future users to follow.

## Week 3: Git Workflow and Repository Process
I then worked on the Git workflow documentation so that everything was properly organized and managed in GitHub with fewer issues. This included reviewing how the project was being tracked, improving the documentation for the workflow, and making sure the process was clearer for contributors.

Together with my brother, we created a dev branch so that work could be tested before being committed to main. This was an important step in establishing a more stable development process. We ran into several issues while setting it up and figuring out the correct workflow, but after troubleshooting and testing, we were able to get it working properly. This also aligned the Git process with the Docker dev container setup, which made the workflow much easier to manage.

## Week 4: Repository Cleanup and Organization
By this point, I began a large cleanup of the repository to make it more professional and easier to navigate. I organized the files, removed unnecessary content, deleted items that were no longer needed, and added ignore rules to prevent clutter from generated or unneeded files.

This cleanup was important because it improved the overall quality and professionalism of the project. It also made the repository easier to understand for both current contributors and anyone who may join the project later. A cleaner structure made the project more maintainable and easier to work on as development continued.

## Teensy and ESP32 Work
After the repository cleanup, I began working on the Teensy and ESP32 setup. This involved learning how to attach the devices, run code, update the firmware, and understand the hardware communication process in a practical setting.

One of the primary issues we encountered was the problem of uploading firmware from the Docker container. PlatformIO was successfully building the firmware, but the upload failed with the following error:

```text
Found device but unable to open
Error opening USB device: Resource temporarily unavailable
```

We traced this issue to the Teensy being passed through multiple USB environments:

```text
Windows → WSL 2 → Docker Desktop → VS Code Dev Container
```

The HalfKay bootloader was visible, but the loader inside Docker could not reliably open it.

To solve this, we changed the workflow so that the firmware was built in the VS Code/Docker environment, copied to WSL, and then uploaded using teensy_loader_cli in WSL before the device was connected to the Teensy.

The revised workflow was:

```text
VS Code / Docker
      │
      ▼
PlatformIO builds firmware.hex
      │
      ▼
Copy HEX to WSL
      │
      ▼
teensy_loader_cli in WSL
      │
      ▼
Teensy 4.1
```

The successful flash output was:

```text
Found HalfKay Bootloader
Programming..................
Booting
```

After that, the Teensy appeared as:

```text
16c0:0483 Van Ooijen Technische Informatica Teensyduino Serial
```

We then verified the firmware by reading the serial output:

```text
Teensy 4.1 heartbeat
```

At that point, the physical Teensy, USB cable, WSL forwarding, firmware build, flash process, and serial communication were all working correctly. This was a major milestone because it confirmed that the embedded system setup was functioning as expected and gave us a stable foundation for future firmware development.

## Additional Learning and Research
Alongside the project work, I have been watching robotics videos to help build familiarity with the hardware, software, mathematics, and broader concepts involved in robotics. This has helped me gain a better understanding of how robotic systems work together and how the various components connect in a practical sense.

I have also been researching different types of filaments and learning how to calibrate them properly so that I can move more directly into successful 3D printing. This has included studying material behavior, print settings, and the steps needed to improve print quality and repeatability.

In addition, I found an app called Kiri Engine, which can be used for 3D scanning and creating models from a phone. I used this to design and create a turntable for easier and clearer photography of objects and to create a clean background for better results. While the app is not the best option available because it is free, it is still useful for quick scanning and object capture. The turntable allowed for more consistent image capture, which made the scanning process more reliable and improved the quality of the results.

I have also been working to understand the overall workflow for preparing and capturing objects so the scans are easier to interpret and use later in the project.

## Ongoing Work
At this stage, the project is continuing to move forward through a combination of technical setup, embedded testing, environment organization, and research. The work completed so far has focused on establishing a solid foundation, and the project is now in a stronger position for continued development in the coming weeks.
