import React, { Fragment, useEffect, useState } from 'react';
import { set, useForm } from "react-hook-form";
import Form from "react-bootstrap/Form";
import Button from 'react-bootstrap/Button';
import BaseAuthPage from './BaseAuthPage';
import { emailRegex } from './utils/regex';
import Stack from 'react-bootstrap/Stack';
import { Link } from 'react-router-dom';

export default function Login() {
  const { register, handleSubmit, formState: {errors} } = useForm();
  const [located, setLocated] = useState(false);
  const [locationInfo, setLocationInfo] = useState({});

  function handleLogin(data) {
    console.log(locationInfo);
  }

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(function(position) {
      if (position) {
        setLocationInfo(position);
        setLocated(true)
      }
    });
  }, [setLocated, setLocationInfo])

  const [passwordVisible, setPasswordVisible] = useState(false)
  const loginForm = <Fragment>
    <Form className='form' onSubmit={(e) => e.preventDefault()}>
      <h2 className='form-header text-secondary'>SIMPLE-Login</h2>
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

      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control 
          type={passwordVisible? "text":"Password"} 
          placeholder="password"
          {...register("password", {
            required: "This field is required"
          })}
          className = "form-input"
        />
         {errors?.password && <Form.Text className="text-danger">
          {errors?.password.message}
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
          onClick={handleSubmit(handleLogin)}
          variant={located? "primary": "primary disabled"} 
          type="submit">
          Submit
        </Button>
        <Form.Text className='text-info'>
          Your location access is needed
        </Form.Text>
      </Stack>
      <Stack>
        <h6 className='text-muted mt-4'>No account yet?<Link to = "/register"> Register here</Link></h6>
      </Stack>
    </Form>
  </Fragment>
  return (
    <BaseAuthPage form={loginForm} />
  )
}
