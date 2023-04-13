# gdsc-backend
Implementation of a CRUD operation with user authentication for a social media platform using a database such as MySQL, ensuring that users can only access and modify their own posts

For Likes Create a like function which see's your username/id and mid of the message you like and increments the like counter (alternately we can create a list starting with null and if username not in like then they can like and  their name is added to the list else it doesn't add your name to the like counter and shows a messsage sayign already liked (optional) the length of the list +1 is the no. of likes

For followers, we can implement it again using lists and then we loop through the usernames one follows and then while getting data from back end, sort it so that only if username is in follower list it gets pulled and presented.

