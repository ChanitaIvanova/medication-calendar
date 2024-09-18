import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Typography, CircularProgress, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Button, Snackbar } from '@mui/material';
import MedicationForm from './MedicationForm';
import { MedicationFormData } from './Medication';
import axios from 'axios';

const EditMedication: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [medication, setMedication] = useState<MedicationFormData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [editedData, setEditedData] = useState<MedicationFormData | null>(null);
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  useEffect(() => {
    fetchMedication();
  }, [id]);

  const fetchMedication = async () => {
    try {
      const response = await axios.get(`/api/medications/medication/${id}`);
      setMedication({
        name: response.data.name,
        contents: response.data.contents,
        objective: response.data.objective,
        sideEffects: response.data.side_effects,
        dosageSchedule: response.data.dosage_schedule,
      });
    } catch (error) {
      setError('Failed to fetch medication data');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (data: MedicationFormData) => {
    setEditedData(data);
    setConfirmDialogOpen(true);
  };

  const handleConfirmEdit = async () => {
    if (!editedData) return;

    setLoading(true);
    try {
      await axios.put(`/api/medications/medication/${id}`, editedData);
      setSnackbarOpen(true);
      setTimeout(() => {
        navigate(`/medications/${id}`);
      }, 2000);
    } catch (error) {
      setError('Failed to update medication');
      setLoading(false);
    }
    setConfirmDialogOpen(false);
  };

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Edit Medication</Typography>
      {medication && (
        <MedicationForm
          onSubmit={handleSubmit}
          initialData={medication}
          submitButtonText="Update Medication"
          isManualInput={true}
          hideToggle={true}
        />
      )}
      <Dialog open={confirmDialogOpen} onClose={() => setConfirmDialogOpen(false)}>
        <DialogTitle>Confirm Edit</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to update this medication?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleConfirmEdit} color="primary">Confirm</Button>
        </DialogActions>
      </Dialog>
      <Snackbar
        open={snackbarOpen}
        message="Medication updated successfully"
        autoHideDuration={2000}
      />
    </Box>
  );
};

export default EditMedication;