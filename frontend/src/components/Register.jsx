import React, { Fragment, useState } from 'react';
import { useForm } from "react-hook-form";
import Form from "react-bootstrap/Form";
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';
import Stack from 'react-bootstrap/Stack';
import ToastContainer from 'react-bootstrap/ToastContainer';
import { BsFillCheckCircleFill } from "react-icons/bs"
import Toast from 'react-bootstrap/Toast';
import BaseAuthPage from './BaseAuthPage';
import { emailRegex, passwordRegex } from './utils/regex';
import { Link } from 'react-router-dom';
import axios from "../api/request";


export default function Register() {
  const { register, handleSubmit, watch, reset, formState: {errors} } = useForm();
  const [passwordMatch, setPasswordMatch] = useState(false);
  const [message, setMessage] = useState({});
  const [loading, setLoading] = useState(false);
  const [showToast, setShowToast] = useState(false);
  
  async function handleRegister(data) {
    setLoading(true);
    try {
        const response = await axios.post("/auth/register",
          {
            "email": data.email,
            "password": data.password
          },
          {
            headers: {
              "Content-type": "application/json"
            },
          }
        );
        setLoading(false)
          setMessage({
            "text": "Account creation success",
            "status": "success"
          });
          setShowToast(true)
          console.log(response.data);
        
    } catch(error) {
      setLoading(false)
      setMessage({
        "text": error.response.data.detail,
        "status": "danger",
      });
      setShowToast(true)
    }
  }

  function checkPassword() {
    const data = watch()
    if(data.password === data.password2) {
      setPasswordMatch(true)
    } else {
      setPasswordMatch(false)
    }
}
  const [passwordVisible, setPasswordVisible] = useState(false)
  const registerForm = <Fragment>
    <Form className='form' onSubmit={(e) => e.preventDefault()}>
      <h2 className='form-header text-secondary'>SIMPLE-Register</h2>
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label className='formLabel'>Email address</Form.Label>
        <Form.Control 
          type="email" 
          placeholder="Enter email"
          {...register("email", {
            required: "This is a required field",
            pattern: {
              value: emailRegex,
              message: "The email must follow this roles email@domain.ex"
            }
          })}
          className = "form-input"
        />
        {errors?.email && <Form.Text className="text-danger">
          {errors?.email.message}
        </Form.Text>}
      </Form.Group>

      <Form.Group className="mb-3" controlId="formBasicPassword1">
        <Form.Label>Password</Form.Label>
        <Form.Control 
          type={passwordVisible? "text":"password"} 
          placeholder="password"
          {...register("password", {
            required: "Must follow these roles",
            pattern: {
              value: passwordRegex,
              message: "Must follow these roles"
            }
          })}
          className = "form-input"
          onKeyDown={checkPassword}
          onkeyup = {checkPassword}
        />
         {errors?.password && <>
          <Form.Text className="text-danger">
            {errors?.password.message}
          </Form.Text><br />
          <Form.Text className="text-muted">
          At least 8 characters,
          must include uppercase, lowercase,n umber and a special character.
          </Form.Text>
         </>}
      </Form.Group>
      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label>Confirm password</Form.Label>
        <Form.Control 
          type={passwordVisible? "text":"password"} 
          placeholder="Password again"
          {...register("password2", {
            required: "This field is required"
          })}
          className = "form-input"
          onKeyDown={checkPassword}
          onKeyUp = {checkPassword}
        />
         {errors?.password2 && <Form.Text className="text-danger">
          {errors?.password2.message}
        </Form.Text>}
      </Form.Group>
      <Form.Group className="mb-3" controlId="formBasicCheckbox">
        <Form.Check 
          type="checkbox" 
          label="Show password"
          onClick={()=> setPasswordVisible(!passwordVisible)}
        />
      </Form.Group>
      <Stack>
        <Button
          onClick={handleSubmit(handleRegister)}
          variant={passwordMatch? "primary": "primary disabled"} 
          type="submit">
          Submit
          {loading && <Spinner
            as="span"
            animation="grow"
            size="sm"
            role="status"
            aria-hidden="true"
            className = "me-2"
          />}
        </Button>
      </Stack>
      <Stack>
        <h6 className='text-muted mt-4'>Account already?<Link to = "/login"> login here</Link></h6>
      </Stack>
    </Form>
  </Fragment>
  const toast = <ToastContainer className='toast-position' position="top-end">
    <Toast onClose={() => setShowToast(false)} show={showToast} delay={6000} autohide>
      <Toast.Header>
        <BsFillCheckCircleFill className={`me-2 text-${message?.status}`} />
        <strong className="me-auto">Notification</strong>
      </Toast.Header>
      <Toast.Body>{message?.text}</Toast.Body>
    </Toast>
  </ToastContainer>
  return (
    <>
      <BaseAuthPage form={registerForm} toast = {toast} />
    </>
  )
}
