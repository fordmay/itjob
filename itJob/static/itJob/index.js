score();
side_history();

document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("#edit_profile_photo").onclick = () => {
    edit_profile_photo();
  }
  document.querySelector("#edit_profile_description").onclick = () => {
    edit_profile_description();
  }
  document.querySelector("#edit_profile_skills").onclick = () => {
    edit_profile_skills();
    remove_button();
  }
});

function edit_profile_photo() {
  const start_src = document.querySelector("#example_pic").src;
  document.querySelector("#modal_01").style.display = "block";
  document.querySelector("#close_01").onclick = () => {
    document.querySelector("#modal_01").style.display = "none";
    document.querySelector("#example_pic").src = start_src;
    // Clear an HTML image input
    document.querySelector("#profile_pic").value = "";
  }
  // Preview an image before it is uploaded
  document.querySelector("#profile_pic").onchange = () => {
    const [file] = document.querySelector("#profile_pic").files;
    if (file) {
      document.querySelector("#example_pic").src = URL.createObjectURL(file);
    }
  }
  // document.querySelector("#save_01").onclick = () => {

  //   fetch(`/posts/${post_id}`, {
  //     method: 'POST',
  //     body: new_value
  //   }).then(result => {
  //     if (result.ok) {
  //       editable_item.innerHTML = new_value;
  //       item.style.display = "block";
  //     }
  //   }).catch(error => {
  //     console.log('Error:', error);
  //   });
  // }
}

function edit_profile_description() {
  document.querySelector("#modal_02").style.display = "block";
  document.querySelector("#close_02").onclick = () => {
    document.querySelector("#modal_02").style.display = "none";
    tinymce.get('textarea').setContent(tinymce.get('textarea').startContent);
  }
  // document.querySelector("#save_02").onclick = () => {
  //   console.log("click")
  //   fetch("/profile/save_description", {
  //     method: "POST",
  //     body: "Hello",
  //     csrfmiddlewaretoken: '{{ csrf_token }}' 
  //   }).then(result => {
  //     if (result.ok) {
  //       console.log("ok")
  //     }
  //   }).catch(error => {
  //     console.log("Error:", error);
  //   });
  // }
}

function edit_profile_skills() {
  document.querySelector("#modal_03").style.display = "block";
  const list_skills = document.querySelector("#table_skills_choses");
  const start_skills = list_skills.innerHTML;
  document.querySelector("#close_03").onclick = () => {
    document.querySelector("#modal_03").style.display = "none";
    list_skills.innerHTML = start_skills;
  }
  document.querySelector("#add_skill_button").onclick = () => {
    const new_skill = document.createElement("tr");
    new_skill.innerHTML = '<td class="skill_choses"><input autofocus class="form-control" type="text" placeholder="Skill"></td><td class="score_choses"><select class="form-select"><option value="0" selected>0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option></select></td><td class="skill_remove"><div class="d-grid gap-2"><button class="btn btn-dark skill_remove_button" type="submit"><strong>-</strong></button></div></td>';
    list_skills.insertBefore(new_skill, list_skills.children[list_skills.children.length - 1])
    remove_button();
  }
}

// Add listener to remove button
function remove_button() {
  document.querySelectorAll(".skill_remove_button").forEach((button) => {
    button.addEventListener('click', () => {
      button.parentElement.parentElement.parentElement.remove();
    });
  });
}

function score() {
  const score = document.querySelectorAll(".score");
  for (let i = 0; i < score.length; i++) {
    score[i].innerHTML = number_to_stars(score[i].innerHTML);
  }
}

function number_to_stars(number) {
  let stars_score = "";
  for (let i = 1; i <= 5; i++) {
    if (i <= number) {
      stars_score = stars_score + "<span class='fa fa-star checked'></span>";
    } else {
      stars_score = stars_score + "<span class='fa fa-star'></span>";
    }
  }
  return stars_score;
}

function side_history() {
  const container_history = document.querySelectorAll(".container-history");
  for (let i = 0; i < container_history.length; i++) {
    if (i % 2 === 0) {
      container_history[i].classList.add("right");
    } else {
      container_history[i].classList.add("left");
    }
  }
}