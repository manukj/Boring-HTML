<html>

<head>

    <!-- shadow and fadein animation -->
    <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/animation.css') }}">
    <!-- lootifie json file -->
    <script src="{{ url_for('static', filename="java_script/lootifie.js")}}"></script>
    <!-- bootstrap css   -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        <!-- font  -->
    <link href="https://fonts.googleapis.com/css?family=Libre+Baskerville&display=swap" rel="stylesheet">


    <title>
        Dashboard
    </title>
</head>
<style>
    * {
        font-family: 'Roboto Slab', serif;
    }

    .container-fluid {
        height: 100%;
        padding: 50px
    }

    .row {
        height: 100%;
        width: 100%;
        margin-left: 0px;
    }

    .upper {
        height: 60%;
        width: 100%;
    }

    .lower {
        height: 40%;
        width: 100%;
        overflow: auto;
        white-space: nowrap;

    }


    .name {
        padding-left: 50px;
        border-right: 1px #afa9a9 solid;
    }

    #profile_name,
    #Project_name {
        letter-spacing: 3px;
        font-family: 'Roboto Slab', serif;
        font-size: 55px
    }

    #total_project {
        letter-spacing: 3px;
        font-family: 'Roboto Slab', serif;
        font-size: 45px
    }

    .lower .card {
        height: 90%;
        width: 20em;
        margin: 10px;
        margin-top: 10px;
        display: inline-block;


    }

    #project_demo {
        width: 100%;
        height: 98%;
        object-fit: cover;
        border-radius: 50% 50% 50% 0%
    }

    input[type='button'] {
        width: 200px;
        font-size: 20px;

    }

    .col-12>.card:hover {
        border-bottom: 6px rgb(95, 95, 95) solid;
        border: 2;


    }

    #project_screen {
        animation: 2s;
    }

    #camera_video_screen {
        animation: 2s;
    }

    input[type="file"] {
        width: 0px;
        height: 0px;
    }

    .crusor {
        cursor: pointer;
    }


    /* width */
    ::-webkit-scrollbar {
        width: 51px;
    }

    /* Track */
    ::-webkit-scrollbar-track {

        border-radius: 10px;
    }

    /* Handle */
    ::-webkit-scrollbar-thumb {
        background: black;
    }

    /* Handle on hover */
    ::-webkit-scrollbar-thumb:hover {
        background: #353535;
    }
</style>

<script>
    window.addEventListener('load', function () {
        //  hide project_screern
        document.getElementById("project_screen").style.visibility = "hidden";
        document.getElementById("project_screen").style.height = "0%";
    })



    // function to taggle between screens
    function showUpload() {
        //  hide project_screern
        document.getElementById("project_screen").style.visibility = "hidden";
        document.getElementById("project_screen").style.height = "0%";
        document.getElementById("project_screen").style.animationName = "";
        // show upload screen
        document.getElementById("camera_video_screen").style.visibility = "visible";
        document.getElementById("camera_video_screen").style.height = "100%";
        document.getElementById("camera_video_screen").style.animationName = "fadeIn";

    }
    function showProject(a) {

        //  show project_screern
        document.getElementById("project_screen").style.visibility = "visible";
        document.getElementById("project_screen").style.height = "100%";
        document.getElementById("project_screen").style.animationName = "fadeIn";
        // hide upload screen
        document.getElementById("camera_video_screen").style.visibility = "hidden";
        document.getElementById("camera_video_screen").style.height = "0%";
        document.getElementById("camera_video_screen").style.animationName = "";

        document.getElementById("project_demo").src = "dummy_image/project.jpeg"
    }
    // end of taggle functions


    function upload(a) {
        document.write(document.getElementById("file-upload").files[0].name);
    }

</script>

<body>
    <div class="container-fluid  fadeInDown " style="animation-duration: 1s">
        <div class="row shadow-lg">
            <div class="col-12 upper">
                <div class="row">
                    <div class="col-3 bg-white name align-self-center ">
                        <p id="profile_name">Manu K J </h1><br>
                            <p id="total_project"> 25 <b style="font-size: 15px">Projetcs</b></p>
                            <a href="index.html" class="text-body stretched-link" style="font-size: 15px">Logout</a>
                    </div>
                    <div class="col-9  p-2 ">
                        <!-- camera_video_screen  -->
                        <div class="col " id="camera_video_screen">
                            <div class="row" style="height: 100%">
                                <div class="col  align-self-center border-right">
                                    <p class="text-center  " style="font-size: 25px">
                                        Upload Image
                                    </p>

                                    <label for="file-upload" class="crusor" style="width: 100%; height: 400px;">
                                        <lottie-player src="json_file/upload.json" background="transparent" speed="1"
                                            autoplay loop>
                                        </lottie-player>
                                    </label>
                                    <input id="file-upload" type="file" onchange="upload()" />


                                </div>
                                <div class="col  align-self-center" onclick="">
                                    <p class="text-center " style="font-size: 25px">

                                        Live Video
                                    </p>
                                    <a href="#">
                                        <lottie-player src="json_file/coming.json" background="transparent" speed="1"
                                            style="width: 100%; height: 400px;" autoplay loop>
                                        </lottie-player>
                                    </a>
                                </div>
                            </div>

                        </div>
                        <!-- end of camera_video_screen -->
                        <!-- project demo screen  -->
                        <div class="col" id="project_screen">
                            <div class="row">
                                <div class="col align-self-center ">
                                    <div class="card-body">
                                        <h5 class="card-title">Project 1</h5>
                                        <h6 class="card-subtitle mb-2 text-muted">28/19/2019</h6>
                                        <p class="card-text">small description about the project .</p>
                                    </div>
                                </div>
                                <div class="col-8">
                                    <img class="border animated  fadeIn" id="project_demo"
                                        src="dummy_image/project.jpeg">

                                </div>
                            </div>
                            <!-- end of project demo sceen  -->
                        </div>
                    </div>
                </div>

            </div>

            <div class="col-12 lower border-top">

                <!-- each project  -->

                <div class="card shadow crusor" onmouseover="showProject(1)" onmouseout="showUpload()"
                    onclick="window.location.href='edit.html'">
                    <img src="dummy_image/project.jpeg" class="card-img-top" style="height: 50%" alt="...">
                    <div class="card-body">
                        <h5 class="card-title">Project 1</h5>
                        <h6 class="card-subtitle mb-2 text-muted">28/19/2019</h6>
                        <p class="card-text">small description about the project .</p>
                    </div>
                </div>

                <div class="card shadow crusor" onmouseover="showProject(1)" onmouseout="showUpload()"
                    onclick="window.location.href='edit.html'">
                    <img src="dummy_image/project.jpeg" class="card-img-top" style="height: 50%" alt="...">
                    <div class="card-body">
                        <h5 class="card-title">Project 1</h5>
                        <h6 class="card-subtitle mb-2 text-muted">28/19/2019</h6>
                        <p class="card-text">small description about the project .</p>
                    </div>
                </div>

                <div class="card shadow crusor" onmouseover="showProject(1)" onmouseout="showUpload()"
                    onclick="window.location.href='edit.html'">
                    <img src="dummy_image/project.jpeg" class="card-img-top" style="height: 50%" alt="...">
                    <div class="card-body">
                        <h5 class="card-title">Project 1</h5>
                        <h6 class="card-subtitle mb-2 text-muted">28/19/2019</h6>
                        <p class="card-text">small description about the project .</p>
                    </div>
                </div>

                <div class="card shadow crusor" onmouseover="showProject(1)" onmouseout="showUpload()"
                    onclick="window.location.href='edit.html'">
                    <img src="dummy_image/project.jpeg" class="card-img-top" style="height: 50%" alt="...">
                    <div class="card-body">
                        <h5 class="card-title">Project 1</h5>
                        <h6 class="card-subtitle mb-2 text-muted">28/19/2019</h6>
                        <p class="card-text">small description about the project .</p>
                    </div>
                </div>

                <div class="card shadow crusor" onmouseover="showProject(1)" onmouseout="showUpload()"
                    onclick="window.location.href='edit.html'">
                    <img src="dummy_image/project.jpeg" class="card-img-top" style="height: 50%" alt="...">
                    <div class="card-body">
                        <h5 class="card-title">Project 1</h5>
                        <h6 class="card-subtitle mb-2 text-muted">28/19/2019</h6>
                        <p class="card-text">small description about the project .</p>
                    </div>
                </div>

                <div class="card shadow crusor" onmouseover="showProject(1)" onmouseout="showUpload()"
                    onclick="window.location.href='edit.html'">
                    <img src="dummy_image/project.jpeg" class="card-img-top" style="height: 50%" alt="...">
                    <div class="card-body">
                        <h5 class="card-title">Project 1</h5>
                        <h6 class="card-subtitle mb-2 text-muted">28/19/2019</h6>
                        <p class="card-text">small description about the project .</p>
                    </div>
                </div>




            </div>
        </div>
    </div>
</body>



</html>