import React from "react";
import { Menu } from "antd";
import { HomeOutlined } from "@ant-design/icons";
import { Link } from "react-router-dom";

const TopNavbar = () => {
  return (
    <Menu mode="horizontal" theme="dark">
      <Menu.Item key="logo" style={{ display: "flex", alignItems: "center" }}>
        {/* <img
                    src="/path-to-your-logo.png" 
                    alt="Logo"
                    style={{ height: 30, width: 30, marginRight: 10 }}
                /> */}
        Aalain Cube
      </Menu.Item>
      <Menu.Item key="home" icon={<HomeOutlined />}>
        <Link to="/">Right Move</Link>
      </Menu.Item>
      {/* <Menu.Item key="about" icon={<AppstoreAddOutlined />}>
        <Link to="/about">About</Link>
      </Menu.Item> */}
    </Menu>
  );
};

export default TopNavbar;
