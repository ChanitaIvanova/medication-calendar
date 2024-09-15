import React, { useState } from 'react';
import axios from 'axios';
import MedicationForm from './MedicationForm';
import { Box } from '@mui/material';

export interface MedicationFormData {
  name: string;
  contents: string;
  objective: string;
  sideEffects: string;
  dosageSchedule: string;
}

const Medicine: React.FC = () => {
  const [isManualInput, setIsManualInput] = useState(true);

  const handleSubmit = async (data: MedicationFormData | File) => {
    let endpoint = '';
    let payload;
    let config = {};

    if (isManualInput) {
      endpoint = '/api/medications/medication';
      payload = data as MedicationFormData;
      config = {
        headers: { 'Content-Type': 'application/json' }
      };
    } else {
      endpoint = '/api/medications/medication/upload';
      payload = new FormData();
      payload.append('file', data as File);
    }

    try {
      const response = await axios.post(endpoint, payload, config);

      if (response.status === 200) {
        console.log('Medicine data submitted successfully');
        // Handle success (e.g., show a success message, reset form, etc.)
      } else {
        console.error('Failed to submit medicine data');
        // Handle error (e.g., show error message)
      }
    } catch (error) {
      console.error('Error submitting medicine data:', error);
      // Handle error (e.g., show error message)
    }
  };

  return (
    <Box>
      <MedicationForm
        onSubmit={handleSubmit}
        onToggleChange={setIsManualInput}
        isManualInput={isManualInput}
      />
    </Box>
  );
};

export default Medicine;