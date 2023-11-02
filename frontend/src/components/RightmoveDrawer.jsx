import { FileAddOutlined } from "@ant-design/icons";
import {
  Button,
  Col,
  Drawer,
  Input,
  List,
  Row,
  Skeleton,
  Space,
  message,
} from "antd";
import React, { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "react-query";
import api from "../common/api";

const RightmoveDrawer = ({ onClose, open, selectedProperty }) => {
  const [newNote, setNewNote] = useState("");
  const queryClient = useQueryClient();
  function handleAddNote() {
    if (newNote !== "") {
      let note = {
        property: selectedProperty.id,
        text: newNote,
      };

      setNewNote("");

      add_new_note_mutation.mutateAsync(note).then((_) => {
        queryClient.invalidateQueries("properties");
      });
    }
  }

  const property_id = selectedProperty?.id;

  const notes_query = useQuery(
    ["notes", property_id],
    async () => {
      return api.get(`/api/rightmove/properties/${property_id}/notes/`);
    },
    {
      enabled: !!property_id,
    }
  );

  const add_new_note_mutation = useMutation({
    mutationFn: (note) => {
      return api.post("/api/rightmove/notes/", note);
    },
    onSuccess: (resp) => {
      queryClient.invalidateQueries("notes");
      queryClient.invalidateQueries("properties");

      message.success("New Note Added");
    },
  });
  const delete_note_mutation = useMutation({
    mutationFn: (note_id) => {
      return api.delete(`/api/rightmove/notes/${note_id}/`);
    },
    onSuccess: (resp) => {
      queryClient.invalidateQueries("notes");
      queryClient.invalidateQueries("properties");
      message.success("Note Deleted");
    },
  });

  if (notes_query.isLoading) {
    return (
      <>
        <Skeleton active />
        <Skeleton active />
        <Skeleton active />
      </>
    );
  }

  return (
    <>
      <Drawer title="Notes" placement="right" onClose={onClose} open={open}>
        <Space>
          <Row style={{ justifyContent: "space-between" }}>
            <Col xs={20}>
              <Input
                placeholder="Add a new note"
                value={newNote}
                onChange={(e) => setNewNote(e.target.value)}
                style={{ width: "100%" }}
              />
            </Col>
            <Col xs={3}>
              <Button
                type="primary"
                onClick={handleAddNote}
                icon={<FileAddOutlined />}
              />
            </Col>
          </Row>
        </Space>

        <List
          style={{ marginTop: 20, width: 300 }}
          bordered
          dataSource={notes_query?.data?.data}
          renderItem={(note, index) => (
            <List.Item
              key={index}
              actions={[
                <Button
                  type="link"
                  onClick={() => delete_note_mutation.mutate(note.id)}
                >
                  Delete
                </Button>,
              ]}
            >
              {note.text}
            </List.Item>
          )}
        />
      </Drawer>
    </>
  );
};

export default RightmoveDrawer;
