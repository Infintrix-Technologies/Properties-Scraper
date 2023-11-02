import React, { useState } from "react";
import { Button, Image, Popconfirm, Table, message } from "antd";
import { useMutation, useQuery, useQueryClient } from "react-query";
import { Link } from "react-router-dom";
import { DeleteOutlined, PaperClipOutlined } from "@ant-design/icons";
import dayjs from "dayjs";
import RightmoveDrawer from "./RightmoveDrawer";
import api from "../common/api";

const Rightmovetable = () => {
  const [open, setOpen] = useState(false);
  const [selectedProperty, setSelectedProperty] = useState({});
  const queryClient = useQueryClient();

  const properties_query = useQuery("properties", async () => {
    return api.get("/api/rightmove/properties/");
  });

  const area_query = useQuery("areas", async () => {
    return api.get("/api/rightmove/areas/");
  });
  const showDrawer = (property) => {
    setSelectedProperty(property);
    setOpen(true);
  };

  const onClose = () => {
    setOpen(false);
  };

  const delete_property_mutation = useMutation({
    mutationFn: (property_id) => {
      return api.delete(`/api/rightmove/properties/${property_id}/`);
    },
    onSuccess: (resp) => {
      queryClient.invalidateQueries("properties");
      message.success("Property deleted Successfuly");
    },
  });

  const data = [
    // {
    //     title: 'id',
    //     dataIndex: 'property_id',
    //     key: 'id',
    //     sorter: (a, b) => a.property_id.localeCompare(b.property_id),

    // },
    {
      title: "image",
      width: 250,
      key: "image",
      render: (item) => {
        return (
          <>
            <Image width={250} src={item.image} />
          </>
        );
      },
    },
    {
      title: "Beds",
      dataIndex: "bedrooms",
      key: "bedrooms",
      sorter: (a, b) => a.bedrooms - b.bedrooms,
    },

    {
      title: "Baths",
      dataIndex: "bathrooms",
      key: "bathrooms",
      sorter: (a, b) => a.bathrooms - b.bathrooms,
    },
    // {
    //     title: 'Has notes',
    //     key: 'has_notes',
    //     render: (item) => (
    //         <Tag color={item.has_notes ? 'green' : 'red'}>
    //             {item.has_notes ? 'True' : 'False'}
    //         </Tag>
    //     ),
    // },
    {
      title: "Area",
      key: "Area",
      dataIndex: "area_zip",
      filters: area_query.isFetching ? [] : area_query?.data?.data,

      onFilter: (value, record) => record.area_zip === value,
      sorter: (a, b) => a.name.length - b.name.length,

      sortDirections: ["descend"],
    },

    {
      title: "Notes",
      key: "Notes",
      render: (item) => {
        return (
          <>
            <Button
              style={{
                background: item.has_notes && "green",
                color: item.has_notes && "white",
              }}
              onClick={() => showDrawer(item)}
            >
              Notes
            </Button>
          </>
        );
      },
    },
    {
      title: "Display Address",
      dataIndex: "displayAddress",
      key: "displayAddress",
    },
    {
      title: "Property Sub Type",
      dataIndex: "propertySubType",
      key: "propertySubType",
    },
    {
      title: "Price",
      key: "price",
      sorter: (a, b) => a.price - b.price,
      render: (item) => {
        return <>£{Number(item.price)}</>;
      },
    },
    {
      title: "URL",
      key: "propertyUrl",
      render: (item) => (
        <Link to={item.propertyUrl} target="_blank" rel="noreferrer">
          <PaperClipOutlined />
        </Link>
      ),
    },
    {
      title: "Visible Date",
      key: "firstVisibleDate",
      render: (item) => (
        // Format the date using dayjs
        <span>{dayjs(item.firstVisibleDate).format("D MMM YYYY")}</span>
      ),
      sorter: (a, b) =>
        dayjs(a.firstVisibleDate).unix() - dayjs(b.firstVisibleDate).unix(), // Sorting function for the 'firstVisibleDate' column
    },
    {
      title: "Property Full Description",
      dataIndex: "propertyTypeFullDescription",
      key: "propertyTypeFullDescription",
    },
    {
      title: "Added Or Reduced",
      dataIndex: "addedOrReduced",
      key: "addedOrReduced",
    },
    {
      title: "Phone",
      dataIndex: "phoneNumber",
      key: "phoneNumber",
    },
    {
      title: "Branch Display Name",
      dataIndex: "branchDisplayName",
      key: "branchDisplayName",
    },
    {
      title: "Action",

      key: "action",
      fixed: "right",
      width: 100,
      render: (item) => (
        <Popconfirm
          title="Delete the Property"
          description="Are you sure to delete this Property?"
          onConfirm={() => delete_property_mutation.mutate(item.id)}
          onCancel={() => {}}
          okText="Yes"
          cancelText="No"
        >
          <Button type="text" icon={<DeleteOutlined />} danger />
        </Popconfirm>
      ),
    },
  ];
  return (
    <>
      <Table
        scroll={{
          x: 1600,
        }}
        loading={properties_query.isLoading}
        rowKey="id"
        columns={data}
        dataSource={properties_query?.data?.data}
      />
      <RightmoveDrawer
        open={open}
        onClose={onClose}
        selectedProperty={selectedProperty}
      />
    </>
  );
};
export default Rightmovetable;
