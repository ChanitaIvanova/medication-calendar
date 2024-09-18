import React, { useState, ChangeEvent } from 'react';
import {
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Box,
  Typography,
} from '@mui/material';
import { MedicationFormData } from './Medication';

interface MedicationFormProps {
  onSubmit: (data: MedicationFormData | File) => void;
  onToggleChange?: (isManual: boolean) => void;
  isManualInput: boolean;
  initialData?: MedicationFormData;
  submitButtonText?: string;
  hideToggle?: boolean;
}

const MedicationForm: React.FC<MedicationFormProps> = ({
  onSubmit,
  onToggleChange,
  isManualInput,
  initialData,
  submitButtonText = "Submit",
  hideToggle = false,
}) => {
  const [formData, setFormData] = useState<MedicationFormData>(
    initialData || {
      name: '',
      contents: '',
      objective: '',
      sideEffects: '',
      dosageSchedule: '',
    }
  );

  const handleInputChange = (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSubmit(formData);
  };

  const handleToggleChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (onToggleChange) {
      onToggleChange(event.target.checked);
    }
  };

  const handleFileUpload = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onSubmit(file);
    }
  };

  return (
    <Box sx={{ maxWidth: 600, margin: 'auto', padding: 2 }}>
      {!hideToggle && (
        <FormControlLabel
          control={<Switch checked={isManualInput} onChange={handleToggleChange} />}
          label="Manual Input"
        />
      )}

      {isManualInput ? (
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            margin="normal"
            label="Name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            required
          />
          <TextField
            fullWidth
            margin="normal"
            label="Contents"
            name="contents"
            multiline
            rows={4}
            value={formData.contents}
            onChange={handleInputChange}
            required
          />
          <TextField
            fullWidth
            margin="normal"
            label="Objective"
            name="objective"
            multiline
            rows={4}
            value={formData.objective}
            onChange={handleInputChange}
            required
          />
          <TextField
            fullWidth
            margin="normal"
            label="Side Effects"
            name="sideEffects"
            multiline
            rows={4}
            value={formData.sideEffects}
            onChange={handleInputChange}
            required
          />
          <TextField
            fullWidth
            margin="normal"
            label="Dosage Schedule"
            name="dosageSchedule"
            multiline
            rows={4}
            value={formData.dosageSchedule}
            onChange={handleInputChange}
            required
          />
          <Button variant="contained" color="primary" type="submit" sx={{ mt: 2 }}>
            {submitButtonText}
          </Button>
        </form>
      ) : (
        <Box sx={{ mt: 2 }}>
          <Typography variant="body1" gutterBottom>
            Upload a text document (PDF, Word, etc.)
          </Typography>
          <input
            accept=".pdf,.doc,.docx,.txt"
            style={{ display: 'none' }}
            id="raised-button-file"
            type="file"
            onChange={handleFileUpload}
          />
          <label htmlFor="raised-button-file">
            <Button variant="contained" component="span">
              Upload Medicine List
            </Button>
          </label>
        </Box>
      )}
    </Box>
  );
};

export default MedicationForm;