# NYU Photobooth

![Web App build & test](https://github.com/software-students-fall2022/final-project-project5-team2/actions/workflows/web-app.yml/badge.svg)
![Continuous Deployment](https://github.com/software-students-fall2022/final-project-project5-team2/actions/workflows/continuous-deployment.yml/badge.svg)

A fun web app that allows users to share their reactions to randomly generated captions– all related to the student life experience at NYU.

Users can choose to create or not create an account. Those who choose to not create an account will only be able to view other user's posts. Users who choose to log in can view other user's posts, create new posts, and like and comment.

# Links

## [Website link](https://nyu-photobooth-paouu.ondigitalocean.app)

## [Deployment link](https://hub.docker.com/repository/docker/pbaggio/nyu-photobooth/general)

## [Figma Wireframe](https://www.figma.com/file/CidintDmYWmno6iNkZHwbF/NYU-captions-wireframe?node-id=0%3A1&t=206D7WPh5fVNc7kN-1)

## [Presenation Link](https://docs.google.com/presentation/d/1Ubn6vOxnutuBWQ8w-xhLCTijeKEPAHvaUFoQVP3Nqkw/edit#slide=id.g1bc7e5e0943_0_0)

## [Web App on DockerHub](https://hub.docker.com/r/pbaggio/nyu-photobooth)

# Running Photobooth (for Developers) 

## Running locally 
1. Clone repo. 
2. In your local copy of the repo, run the following comamnd in your Terminal:

```console
cd web-app
```

3. Pip3 install all dependencies in [requirements.txt](https://github.com/software-students-fall2022/final-project-project5-team2/blob/main/web-app/requirements.txt) within the web-app directory. 

4. In a .env file in the root directory, establish a connection to a database using a variable named MONGODB_CONNSTRING.

5. Now, when you go to the web-app directory, you can just run the following command: 

```console
flask run
```

to start the server. 

## Using Docker to access server

1. Ensure that Docker is running on your machine. 

2. Run the following command in terminal, in any root directory on your machine

```console
docker pull pbaggio/nyu-photobooth
```

3. Then run the following command in the same chosen directory

```console
docker pull pbaggio/nyu-photobooth
```





# Team members

Pedro Baggio ([Jignifs](https://github.com/Jignifs))

Eduarda Martini ([ezmartini](https://github.com/ezmartini))

Laura Lourenco ([qlaueen](https://github.com/qlaueen))

Lucy Kocharian ([Lkochar19](https://github.com/Lkochar19))
