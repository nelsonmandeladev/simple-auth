import React, { Fragment } from 'react';

export default function BaseAuthPage({form, toast}) {
  return (
    <Fragment>
        <div className="auth">
            <div>{form}</div>
        </div>
        {toast}
    </Fragment>
  )
}
