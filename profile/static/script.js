document.getElementById("profileForm").addEventListener("submit", async (event) => {
    event.preventDefault();
  
    const formData = new FormData();
    formData.append("username", document.getElementById("username").value);
    formData.append("email", document.getElementById("email").value);
    formData.append("bio", document.getElementById("bio").value);
  
    const profilePicture = document.getElementById("profilePicture").files[0];
    if (profilePicture) {
      formData.append("profilePicture", profilePicture);
    }
  
    const response = await fetch("/update_profile", {
      method: "POST",
      body: formData,
    });
  
    const result = await response.json();
    const message = document.getElementById("message");
    if (result.success) {
      message.textContent = "Profile updated successfully!";
      if (result.profile_pic_url) {
        document.getElementById("profilePic").src = result.profile_pic_url;
      }
    } else {
      message.textContent = "Failed to update profile.";
    }
  });
  