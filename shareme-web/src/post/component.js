import React, {useEffect, useState}  from 'react'

import {createPost, loadPosts} from '../lookup'

export function PostsComponent(props) {
    const textAreaRef = React.createRef()
    const [newPosts, setNewPosts] = useState([])
    const handleSubmit = (event) => {
      event.preventDefault()
      const newVal = textAreaRef.current.value
      let tempNewPosts = [...newPosts]
      // change this to a server side call
      createPost(newVal, (response, status)=>{
        if (status === 201){
          tempNewPosts.unshift(response)
        } else {
          console.log(response)
          alert("An error occured please try again")
        }
      })

      setNewPosts(tempNewPosts)
      textAreaRef.current.value = ''
    }
    return <div className={props.className}>
            <div className='col-12 mb-3'>
              <form onSubmit={handleSubmit}>
                <textarea ref={textAreaRef} required={true} className='form-control' name='tweet'>

                </textarea>
                <button type='submit' className='btn btn-primary my-3'>Tweet</button>
            </form>
            </div>
        <PostsList newPosts={newPosts} />
    </div>
}

export function PostsList(props) {
    const [postsInit, setPostsInit] = useState([])
    const [posts, setPosts] = useState([])
    const [postsDidSet, setPostsDidSet] = useState(false)
    useEffect(()=>{
      const final = [...props.newPosts].concat(postsInit)
      if (final.length !== posts.length) {
        setPosts(final)
      }
    }, [props.newPosts, posts, postsInit])

    useEffect(() => {
      if (postsDidSet === false){
        const myCallback = (response, status) => {
          if (status === 200){
           setPostsInit(response)
           setPostsDidSet(true)
          } else {
            alert("There was an error")
          }
        }
       loadPosts(myCallback)
      }
    }, [postsInit, postsDidSet, setPostsDidSet])
    return posts.map((item, index)=>{
      return <Post tweet={item} className='my-5 py-5 border bg-white text-dark' key={`${index}-{item.id}`} />
    })
  }


export function ActionBtn(props) {
    const {post, action} = props
    const [likes, setLikes] = useState(post.likes ? post.likes : 0)
    const [userLike, setUserLike] = useState(post.userLike === true ? true : false)
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.display ? action.display : 'Action'

    const handleClick = (event) => {
      event.preventDefault()
      if (action.type === 'like') {
        if (userLike === true) {
          // perhaps i Unlike it?
          setLikes(likes - 1)
          setUserLike(false)
        } else {
          setLikes(likes + 1)
          setUserLike(true)
        }

      }
    }
    const display = action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay
    return <button className={className} onClick={handleClick}>{display}</button>
  }

export function Post(props) {
    const {post} = props
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    return <div className={className}>
        <p>{post.id} - {post.content}</p>
        <div className='btn btn-group'>
          <ActionBtn post={post} action={{type: "like", display:"Likes"}}/>

          <ActionBtn post={post} action={{type: "re-post", display:""}}/>
        </div>
    </div>
  }