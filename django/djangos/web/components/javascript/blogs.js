document.addEventListener("DOMContentLoaded", function () {
  let editBlogId;
  const blogsUrl = document.getElementById("blogs-blogs")?.getAttribute("data-url");
  const blogBaseUrl = document.getElementById("blogs-blog")?.getAttribute("data-url")?.slice(0, -1);

  if (!blogsUrl || !blogBaseUrl) {
    console.error("Required elements not found in the DOM.");
    return;
  }

  console.log("blogsUrl:", blogsUrl);
  console.log("blogBaseUrl:", blogBaseUrl);

  function fetchBlogs() {
    fetch(blogsUrl, {
      method: "GET",
      headers: getHeaders(),
    })
      .then(response => {
        if (!response.ok) {
          // check for error response and read the error message
          if (response.status == 401) {
            alert("You are not authorized to view this page. Please login. Session expired.");
            window.location.href = "/users/login";
          }
          else {
            throw new Error("Failed to fetch blogs.");
          }
        }
        return response.json();
      })
      .then(data => {
        const blogList = document.getElementById("blogList");
        blogList.innerHTML = "";
        data.reverse().forEach(blog => {
          blogList.innerHTML += `
          <li class="list-group-item" data-id="${blog.id}" data-toggle="modal" data-target="#editBlogModal">
            <a href="#" class="blog-link" data-toggle="modal" data-target="#editBlogModal">${blog.title}</a>
            <p>${truncateContent(blog.content)}</p>
          </li>
        `;
        });
      });
  }


  function getHeaders() {
    return {
      Authorization: localStorage.getItem("access_token"),
      Accept: "application/json",
      "Content-Type": "application/json",
    };
  }

  function truncateContent(content) {
    return content.length > 200 ? content.substring(0, 200) + "..." : content;
  }

  function handleSubmit(url, method, title, content) {
    fetch(url, {
      method: method,
      headers: getHeaders(),
      body: JSON.stringify({ title, content }),
    })
      .then(() => {
        fetchBlogs();
      });
  }


  const addBlogButton = document.getElementById("add-blog");
  if (addBlogButton) {
    addBlogButton.addEventListener("click", function () {
      document.getElementById("editBlogModalLabel").innerText = "Add Blog";
      document.getElementById("editTitle").value = "";
      document.getElementById("editContent").value = "";
      document.getElementById("deleteblog").hidden = true;
      editBlogId = undefined;
    });
  }

  const blogForm = document.getElementById("blogForm");
  if (blogForm) {
    blogForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const title = document.getElementById("title").value;
      const content = document.getElementById("content").value;
      handleSubmit(blogsUrl, "POST", title, content);
    });
  }

  const blogList = document.getElementById("blogList");
  if (blogList) {
    blogList.addEventListener("click", function (e) {
      const listItem = e.target.closest("li.list-group-item");
      if (listItem) {
        editBlogId = listItem.getAttribute("data-id");

        // fetch blog details
        fetch(`${blogBaseUrl}${editBlogId}`, {
          method: "GET",
          headers: getHeaders(),
        })
        .then(response => response.json())
        .then(data => {
          console.log("data in fetchBlog:", data)
          document.getElementById("editTitle").value = data.title;
          document.getElementById("editContent").value = data.content;
        })
        .catch(error => {
          console.error("Error:", error);
        });
        document.getElementById("deleteblog").hidden = false;
      }
    });
  }

  const editBlogForm = document.getElementById("editBlogForm");
  if (editBlogForm) {
    editBlogForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const title = document.getElementById("editTitle").value;
      const content = document.getElementById("editContent").value;
      const method = editBlogId === undefined ? "POST" : "PUT";
      const url = editBlogId === undefined ? blogsUrl : `${blogBaseUrl}${editBlogId}`;
      handleSubmit(url, method, title, content);
    });
  }

  const deleteBlogButton = document.getElementById("deleteblog");
  if (deleteBlogButton) {
    deleteBlogButton.addEventListener("click", function (e) {
      e.preventDefault();
      if (confirm("Are you sure you want to delete this blog?")) {
        fetch(`${blogBaseUrl}${editBlogId}`, {
          method: "DELETE",
          headers: getHeaders(),
        })
          .then(() => {
            fetchBlogs();
          });
      }
    });
  }

  // Fetch blogs on page load
  fetchBlogs();
});
