import { LoadingButton } from "@mui/lab";
import { Box, Typography, useTheme } from "@mui/material";
import React from "react";
import { passwordSuite } from "../../utils/suites/passwordSuite";
import sendRequest from "../../utils/funcs/sendRequest";
import { API_ENDPOINTS, FULL_API_ENDPOINT } from "../../utils/consts";
import { useUser } from "../../context/UserContext";
import { useAlert } from "react-alert";

const PasswordField = () => {
  const alert = useAlert();
  const user = useUser();
  const theme = useTheme();
  const [loading, setLoading] = React.useState<boolean>(false);
  const [passwordFields, setPasswordFields] = React.useState({
    password: "",
    confirm_password: "",
  });
  const [formState, setFormState] = React.useState({});

  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
    currentField: "password" | "confirm_password",
    value: string
  ) => {
    setPasswordFields({
      ...passwordFields,
      [currentField]: event.target.value,
    });
    const nextState = { ...formState, [currentField]: value };
    passwordSuite(nextState, currentField);
    setFormState(nextState);
  };

  const suiteResult = passwordSuite.get();

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await sendRequest(
        "patch",
        FULL_API_ENDPOINT + API_ENDPOINTS.USERS + `${user.id}/`,
        user.accessToken!,
        { ...passwordFields }
      );
      if (response.status == 200) {
        alert.show("Password has changed", { type: "success" });
      } else {
        alert.show("Password could not change", { type: "error" });
      }
    } catch (error: any) {
      alert.show("Error", { type: "error" });
    } finally {
      setLoading(false);
      setPasswordFields({
        password: "",
        confirm_password: "",
      });
      passwordSuite.reset();
    }
  };

  return (
    <Box
      component="form"
      onSubmit={(event) => {
        event.preventDefault();
        handleSubmit();
      }}
    >
      <div className="input-group mb-3">
        <div className="input-group-prepend">
          <span
            style={{
              backgroundColor: theme.palette.mode == "dark" ? "#141414" : "",
              color: theme.palette.mode == "dark" ? "#fefefe" : "black",
            }}
            className="input-group-text"
            id="basic-addon1"
          >
            Password
          </span>
        </div>
        <input
          disabled={loading}
          style={{
            backgroundColor: theme.palette.mode == "dark" ? "black" : "",
            color: theme.palette.mode == "dark" ? "#fafafa" : "black",
          }}
          type="password"
          className="form-control"
          placeholder="Your new password"
          aria-label="Password"
          aria-describedby="basic-addon1"
          value={passwordFields.password}
          onChange={(event) =>
            handleChange(event, "password", event.target.value)
          }
          id="password"
        />
      </div>
      {suiteResult.hasErrors("password") && (
        <Typography fontSize=".9em" marginBottom="1em" color="#8B0000">
          {suiteResult.getErrors("password")[0]}
        </Typography>
      )}
      <div className="input-group mb-3">
        <div className="input-group-prepend">
          <span
            style={{
              backgroundColor: theme.palette.mode == "dark" ? "#141414" : "",
              color: theme.palette.mode == "dark" ? "#fefefe" : "black",
            }}
            className="input-group-text"
            id="basic-addon1"
          >
            Confirm Password
          </span>
        </div>
        <input
          disabled={loading}
          style={{
            backgroundColor: theme.palette.mode == "dark" ? "black" : "",
            color: theme.palette.mode == "dark" ? "#fafafa" : "black",
          }}
          type="password"
          className="form-control"
          placeholder="Your new password again"
          aria-label="Password Confirm"
          aria-describedby="basic-addon1"
          value={passwordFields.confirm_password}
          onChange={(event) =>
            handleChange(event, "confirm_password", event.target.value)
          }
          id="confirm_password"
        />
      </div>
      {suiteResult.hasErrors("confirm_password") && (
        <Typography fontSize=".9em" marginBottom="1em" color="#8B0000">
          {suiteResult.getErrors("confirm_password")[0]}
        </Typography>
      )}
      <LoadingButton
        type="submit"
        sx={{ width: { xs: "60%", sm: "30%", md: "30%" } }}
        variant="contained"
        disabled={!suiteResult.isValid()}
        loading={loading}
      >
        Change Password
      </LoadingButton>
    </Box>
  );
};

export default PasswordField;
