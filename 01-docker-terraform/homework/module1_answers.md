# Module 1 Homework Answers

## Question 1
Run docker with the python:3.12.8 image in an interactive mode, use the entrypoint bash.

What's the version of pip in the image?

**Answer:** 
```bash
docker run -it --entrypoint /bin/bash python:3.12.8
pip --version
